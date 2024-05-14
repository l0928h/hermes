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
    else:
        targets_file = input("Enter the path to the JSON file containing target list: ")
        targets = read_json_file(targets_file)
    return targets.strip()

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Scan results saved to {filename}")

def read_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

# 示例使用
tool_choice = select_tool()
if tool_choice == 'nmap':
    # 获取扫描目标
    nmap_targets = get_targets_from_input()
    print("Nmap Scan Targets:", nmap_targets)
elif tool_choice == 'metasploit':
    # 您的 Metasploit 代码部分，此处省略
    pass