import subprocess
import sys

def run_nmap_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Nmap scan completed successfully. Command: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Nmap scan: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python nmap_script.py <input_filename> <output_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # 构建Nmap命令
    commands = [
        f"nmap -sS -Pn -A -v -iL {input_filename} -oX {output_filename}_full_scan.xml",
        f"nmap -sV -T4 -iL {input_filename} -oX {output_filename}_version_scan.xml",
        f"nmap -p 80,443 --script http-enum --script-args http-enum.category=login -iL {input_filename} -oX {output_filename}_login_pages.xml"
    ]

    # 运行命令
    for command in commands:
        run_nmap_command(command)

if __name__ == "__main__":
    main()
