#!/usr/bin/python3
from fedconcore.main import *
import sys,requests
from colorama import Style,Fore
#=====
def fedconp(args):
    token=open(args[2]).readline().strip('\n')
    temp=args[1].split('@')
    if len(temp)!=2:
        prnt_err('Incorrect user@domain format')
        HELP()
    username=temp[0]
    domain=temp[1]
    Headers={'User-Agent':ua.random,'Authorization':'Bearer '+token}
    res=requests.get(f'https://{domain}/api/v1/timelines/public', headers=Headers)
    try:
        json.loads(res.text)
    except json.decoder.JSONDecodeError:
        prnt_err(f'Provided token in invalid')
        sys.exit()
    basic_info=user_search(username,domain,Headers)
    export_basic_info(basic_info)
    get_user_posts(basic_info['id'],domain,Headers)
    a=input(f'{Fore.YELLOW}[----] {Fore.GREEN}Do you want to search for accounts with the username "{username}" on other PixelFed instances? (Y/N) : ')
    if a.lower()=='y':pixelfedsearch(username)
#=====
print(Style.BRIGHT)
banner()
if len(sys.argv)<3:
    prnt_err('Requires 2 arguments')
    HELP()
else:
    if os.path.exists(sys.argv[2])==1:fedconp(sys.argv)
    else:prnt_err(f'Token file: "{os.getcwd()}/{sys.argv[2]}" does not exists')