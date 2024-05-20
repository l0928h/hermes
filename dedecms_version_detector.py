import requests
from termcolor import cprint
import re

class DedecmsVersionDetector:
    """A class to detect the version of Dedecms based on the `ver.txt` file."""
    
    def __init__(self, url):
        self.url = 'http://' + url if '://' not in url else url

    def fetch_version(self):
        """Fetches the version from the ver.txt file and prints formatted version information."""
        version_history = {
            '20080307': 'v3 or v4 or v5', '20080324': 'v5 above', '20080807': '5.1 or 5.2',
            '20081009': 'v5.1sp', '20081218': '5.1sp', '20090810': '5.5', '20090912': '5.5',
            '20100803': '5.6', '20101021': '5.3', '20111111': 'v5.7 or v5.6 or v5.5', 
            '20111205': '5.7.18', '20111209': '5.6', '20120430': '5.7SP or 5.7 or 5.6', 
            '20120621': '5.7SP1 or 5.7 or 5.6', '20120709': '5.6', '20121030': '5.7SP1 or 5.7', 
            '20121107': '5.7', '20130608': 'V5.6-Final', '20130922': 'V5.7SP1', '20140225': 'V5.6SP1',
            '20140725': 'V5.7SP1', '20150618': '5.7', '20180109': 'V5.7SP2'
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Accept-Encoding": "gzip, deflate"
        }
        response = requests.get(f"{self.url}/data/admin/ver.txt", headers=headers)
        if response.status_code == 200:
            version_number = re.search(r"^\d+$", response.text.strip())
            if version_number:
                version_key = version_number.group()
                if version_key in version_history:
                    version = version_history[version_key]
                else:
                    version = "Unknown version"
                cprint(f"Dedecms version detected: {response.text.strip()} -> {version}", "red")
            else:
                cprint("No version number found in the ver.txt.", "yellow")
        else:
            cprint(f"Failed to retrieve ver.txt. Status Code: {response.status_code}", "yellow")

# Example usage
if __name__ == "__main__":
    domain = input("Please enter a domain to check (e.g., example.com): ")
    detector = DedecmsVersionDetector(domain)
    detector.fetch_version()

