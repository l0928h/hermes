import requests
from termcolor import cprint
import re
import json

class DedecmsVersionDetector:
    def __init__(self, url):
        if '://' not in url:
            self.url = 'http://' + url
        else:
            self.url = url

    def fetch_version(self):
        version_history = {
            '20080307': {'version': 'v3 or v4 or v5'}, 
            '20080324': {'version': 'v5 above'}, 
            '20080807': {'version': '5.1 or 5.2'},
            '20081009': {'version': '5.1sp'}, 
            '20081218': {'version': '5.1sp'}, 
            '20090810': {'version': '5.5'}, 
            '20090912': {'version': '5.5'},
            '20100803': {'version': '5.6'}, 
            '20111015': {'version': '5.7.15'}, 
            '20111015': {'version': '5.7.15'}, 
            '20111111': {'version': '5.7.16'}, 
            '20111227': {'version': '5.7.17'}, 
            '20120430': {'version': '5.7.18'},
            '20120621': {'version': '5.7.19'}, 
            '20121030': {'version': '5.7.20'},
            '20121122': {'version': '5.7.22'},
            '20121218': {'version': '5.7.23'},
            '20130115': {'version': '5.7 24'},
            '20130121': {'version': '5.7 25'},
            '20130401': {'version': '5.7 26'},
            '20130402': {'version': '5.7 27'},
            '20130422': {'version': '5.7 28'},
            '20130606': {'version': '5.7 29'}, 
            '20130607': {'version': '5.7.30'},
            '20130715': {'version': '5.7 31'}, 
            '20130922': {'version': '5.7 32'},
            '20140114': {'version': '5.7.33'},
            '20140115': {'version': '5.7.34'},
            '20140116': {'version': '5.7.35'}, 
            '20140225': {'version': '5.7.36'},
            '20140228': {'version': '5.7.37'},
            '20140304': {'version': '5.7.38'},
            '20140305': {'version': '5.7.39'},
            '20140311': {'version': '5.7.40'},
            '20140313': {'version': '5.7.41'},
            '20140415': {'version': '5.7.42'},
            '20140606': {'version': '5.7.43'},
            '20140612': {'version': '5.7.44'},
            '20140623': {'version': '5.7.45'},
            '20140627': {'version': '5.7.46'},
            '20140724': {'version': '5.7.47'},
            '20140725': {'version': '5.7.48'},  
            '20140814': {'version': '5.7.49'},
            '20150522': {'version': '5.7.50'},
            '20170618': {'version': '5.7.58'},
            '20170726': {'version': '5.7.59'},
            '20170801': {'version': '5.7.60'},
            '20160811': {'version': '5.7.61'},
            '20160816': {'version': '5.7.62'},
            '20160906': {'version': '5.7.63'},
            '20160928': {'version': '5.7.64'},
            '20170303': {'version': '5.7.65'},
            '20170309': {'version': '5.7.66'},
            '20170315': {'version': '5.7.68'},
            '20170330': {'version': '5.7.69'},
            '20170405': {'version': '5.7.70', 'vulnerabilities': ['CVE-2017-17730', 'CVE-2017-17731']},
            '20171228': {'version': '5.7.71'},
            '20180104': {'version': '5.7.72'},
            '20180107': {'version': '5.7.73'},
            '20180109': {'version': '5.7.74', 'vulnerabilities': ['CVE-2018-6910']},
            '20210829': {'version': '5.7.80', 'vulnerabilities': ['CVE-2018-7700']},
            '20210330': {'version': '5.7', 'vulnerabilities': ['CVE-2018-9134']},
            '20210623': {'version': '5.7.75', 'vulnerabilities': ['CVE-2023-2056']},
            '20210712': {'version': '5.7.76', 'vulnerabilities': ['CVE-2023-2056']},
            '20210719': {'version': '5.7.77', 'vulnerabilities': ['CVE-2023-2056']},
            '20210806': {'version': '5.7.78', 'vulnerabilities': ['CVE-2023-2056']},
            '20210815': {'version': '5.7.79', 'vulnerabilities': ['CVE-2023-2056']},
            '20210829': {'version': '5.7.80', 'vulnerabilities': ['CVE-2023-2056']},
            '20210915': {'version': '5.7.81', 'vulnerabilities': ['CVE-2023-2056']},
            '20210926': {'version': '5.7.82', 'vulnerabilities': ['CVE-2023-2056']},
            '20211022': {'version': '5.7.83', 'vulnerabilities': ['CVE-2023-2056']},
            '20211123': {'version': '5.7.84', 'vulnerabilities': ['CVE-2023-2056']},
            '20211224': {'version': '5.7.85', 'vulnerabilities': ['CVE-2023-2056']},
            '20220112': {'version': '5.7.86', 'vulnerabilities': ['CVE-2023-2056']},
            '20220114': {'version': '5.7.87', 'vulnerabilities': ['CVE-2023-2056']},
            '20220125': {'version': '5.7.88'},
            '20220218': {'version': '5.7.89'},
            '20220225': {'version': '5.7.90'},
            '20220310': {'version': '5.7.91'},
            '20220325': {'version': '5.7.92'},
            '20220504': {'version': '5.7.93'},
            '20220520': {'version': '5.7.94'},
            '20220612': {'version': '5.7.95'},
            '20220627': {'version': '5.7.96'},
            '20220708': {'version': '5.7.97'},
            '20220803': {'version': '5.7.98'},
            '20220915': {'version': '5.7.99'},
            '20220920': {'version': '5.7.100'},
            '20220930': {'version': '5.7.101'},
            '20221106': {'version': '5.7.102'},
            '20221207': {'version': '5.7.103'},
            '20220106': {'version': '5.7.104'},
            '20220202': {'version': '5.7.105'},
            '20220223': {'version': '5.7.106', 'vulnerabilities': ['CVE-2023-27709', 'CVE-2024-27707']},
            '20220315': {'version': '5.7.107'},
            '20230428': {'version': '5.7.108'},
            '20230524': {'version': '5.7.109', 'vulnerabilities': ['CVE-2023-37839', 'CVE-2023-34842']},
            '20230630': {'version': '5.7.110'},
            '20230913': {'version': '5.7.111', 'vulnerabilities': ['CVE-2023-43226', 'CVE-2024-34959']},
            '20231201': {'version': '5.7.112'},
            '20240314': {'version': '5.7.113', 'vulnerabilities': ['CVE-2024-33371', 'CVE-2024-34959']},
            '20240413': {'version': '5.7.114', 'vulnerabilities': ['CVE-2024-29660','CVE-2024-29661', 'CVE-2024-34245', 'CVE-2024-33749']},
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept-Encoding": "gzip, deflate"
        }
        try:
            cprint(f"正在扫描网站：{self.url}", "cyan")
            response = requests.get(f"{self.url}/data/admin/ver.txt", headers=headers)
            if response.status_code == 200:
                version_number = re.search(r"^\d{8}$", response.text.strip())
                if version_number:
                    version_key = version_number.group()
                    version_info = version_history.get(version_key, {"version": "Unknown version", "vulnerabilities": []})
                    #
                    vulnerabilities = ", ".join(version_info.get('vulnerabilities', []))
                    if vulnerabilities:
                        message = f"{version_info['version']} ({vulnerabilities})"
                    else:
                        message = f"{version_info['version']} (No known vulnerabilities)"
                    cprint(f"Dedecms version detected: {response.text.strip()} -> {message}", "green")
                
                else:
                    cprint("No version number found in the ver.txt.", "yellow")
            else:
                cprint(f"Failed to retrieve ver.txt. Status Code: {response.status_code}", "yellow")
        except requests.exceptions.RequestException as e:
            cprint(f"Error fetching version information: {e}", "red")

def load_urls_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [item['url'] for item in data]

def main():
    print("欢迎使用 Dedecms 版本检测器")
    print("1. 输入目标网站")
    print("2. 从 JSON 文件批量扫描")
    choice = input("请选择操作（1或2）：")
    
    if choice == '1':
        domain = input("请输入要检测的域名（例如：example.com）：")
        detector = DedecmsVersionDetector(domain)
        detector.fetch_version()
    elif choice == '2':
        file_path = input("请输入 JSON 文件路径（例如：domains.json）：")
        urls = load_urls_from_json(file_path)
        for url in urls:
            detector = DedecmsVersionDetector(url)
            detector.fetch_version()
    else:
        print("无效输入，请重新运行程序并选择 1 或 2。")

if __name__ == "__main__":
    main()













