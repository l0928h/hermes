import subprocess
import argparse
import os
import json

def run_nmap_command(command, target_index, total_targets):
    print(f"Scanning target {target_index} of {total_targets}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Nmap scan for target {target_index} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Nmap scan for target {target_index}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Run selective Nmap scans with progress updates and configurable output location.')
    parser.add_argument('input_filename', help='JSON file containing target URLs')
    parser.add_argument('--output_dir', default='data', help='Directory to save the scan results (default is "data/")')
    parser.add_argument('--full_scan', action='store_true', help='Perform a full intense scan')
    parser.add_argument('--version_scan', action='store_true', help='Perform a service version detection scan')
    parser.add_argument('--login_scan', action='store_true', help='Scan for login pages')
    parser.add_argument('--output_format', choices=['xml', 'txt', 'html'], default='xml', help='Choose the output format of the scan results')

    args = parser.parse_args()

    # Load targets from JSON
    with open(args.input_filename, 'r') as file:
        data = json.load(file)
        targets = [item['url'] for item in data]

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    commands = []
    total_targets = len(targets)
    for index, target in enumerate(targets):
        output_file = os.path.join(args.output_dir, f"{target.replace('.', '_')}_{index + 1}.{args.output_format}")
        if args.full_scan:
            commands.append((f"nmap -sS -Pn -A -v -iL {target} -oX {output_file}", index + 1, total_targets))
        if args.version_scan:
            commands.append((f"nmap -sV -T4 -iL {target} -oX {output_file}", index + 1, total_targets))
        if args.login_scan:
            commands.append((f"nmap -p 80,443 --script http-enum --script-args http-enum.category=login -iL {target} -oX {output_file}", index + 1, total_targets))

    if not commands:
        print("No scans selected. Use --help for more information.")
        sys.exit(1)

    for command, index, total in commands:
        run_nmap_command(command, index, total)

if __name__ == "__main__":
    main()
