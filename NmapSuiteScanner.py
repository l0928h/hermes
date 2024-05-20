import subprocess
import argparse
import os
import json
import sys
from concurrent.futures import ThreadPoolExecutor

def run_nmap_command(command, output_file):
    """
    Executes an Nmap scan command and saves the output to a file.

    Args:
        command (str): The nmap command to execute.
        output_file (str): The path to the output file where results will be saved.
    """
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Nmap scan output saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Nmap scan: {e}")

def main():
    parser = argparse.ArgumentParser(description='Run selective Nmap scans with progress updates and configurable output location.')
    parser.add_argument('input_filename', nargs='?', default='../data/input_websites_list.json', help='JSON file containing target URLs (default is "../data/input_websites_list.json")')
    parser.add_argument('--output_dir', default='results', help='Directory to save the scan results (default is "results/")')
    parser.add_argument('--full_scan', action='store_true', help='Perform a full intense scan')
    parser.add_argument('--version_scan', action='store_true', help='Perform a service version detection scan')
    parser.add_argument('--login_scan', action='store_true', help='Scan for login pages')
    parser.add_argument('--output_format', choices=['xml', 'txt', 'html'], default='xml', help='Choose the output format of the scan results')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads to use for parallel scanning')

    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Load targets from JSON
    try:
        with open(args.input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            targets = [item['url'] for item in data]
    except FileNotFoundError:
        print(f"Error: The file {args.input_filename} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: The file format is invalid. Please provide a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load or parse the input file: {e}")
        sys.exit(1)

    # Generate Nmap commands and execute each scan
    total_targets = len(targets)
    for index, target in enumerate(targets):
        sanitized_target = target.replace(':', '_').replace('/', '_').replace('.', '_')
        output_file = os.path.join(args.output_dir, f"{sanitized_target}_{index + 1}.{args.output_format}")
        command_base = f"nmap -o{args.output_format} {output_file} {target}"
        
        if args.full_scan:
            run_nmap_command(f"{command_base} -sS -Pn -A -v", output_file)
        if args.version_scan:
            run_nmap_command(f"{command_base} -sV -T4", output_file)
        if args.login_scan:
            run_nmap_command(f"{command_base} -p 80,443 --script http-enum --script-args http-enum.category=login", output_file)

if __name__ == "__main__":
    main()









