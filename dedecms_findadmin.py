#
import requests
from termcolor import cprint
import re
import json  # 导入 json 模块处理 JSON 文件

class FindAdmin:
    def __init__(self, url):
        if '://' not in url:
            self.url = 'http://' + url
        else:
            self.url = url

    def find_admin(self):
        characters = "abcdefghijklmnopqrstuvwxyz0123456789_!#"
        admin_path = "/dede"
        admin_url = self.url + admin_path
        try:
            response = requests.get(admin_url, timeout=10)
            cprint(f"Attempted to access {admin_url}", "cyan")  # Debugging output
            if response.status_code == 200:
                cprint(f"Admin directory found: {admin_url}", "green")
                return admin_url
            else:
                cprint(f"Accessed {admin_url} but received HTTP status {response.status_code}", "yellow")
        except requests.exceptions.Timeout:
            cprint(f"Timeout occurred while trying to connect to {admin_url}", "yellow")
        except requests.exceptions.RequestException as e:
            cprint(f"Error fetching admin directory: {e}", "red")

def load_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [item['url'] for item in data]

def main():
    print("1. 输入单个域名进行检查")
    print("2. 从 JSON 文件批量检查域名")
    choice = input("请选择操作方式 (1 或 2): ")
    
    if choice == '1':
        url = input("请输入要检查的域名: ")
        finder = FindAdmin(url)
        finder.find_admin()
    elif choice == '2':
        file_path = input("请输入 JSON 文件路径: ")
        urls = load_urls_from_json(file_path)
        for url in urls:
            finder = FindAdmin(url)
            finder.find_admin()
    else:
        print("无效的输入，请选择 1 或 2。")

if __name__ == "__main__":
    main()





