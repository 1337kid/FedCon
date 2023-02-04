import requests,json,os,shutil,mimetypes,sys,csv
from fake_useragent import UserAgent
from colorama import Fore,Back,Style
import concurrent.futures
from fedconcore.fields import *
#
def prnt_binfo(a,b,c=''):print(f'{c}{Fore.YELLOW} | {Fore.BLUE}{a:<25}: {b}')
def prnt_info(a,b='INFO',c=''):print(f'{c}{Fore.YELLOW}[{b}] {Fore.GREEN}{a}')
def prnt_err(a):
    print(f'{Fore.RED+Back.BLACK}[ERROR] {a}{Style.RESET_ALL}')
def banner():
    print(f'''{Fore.CYAN}
      __              _     ___                   
     / _|   ___    __| |   / __|    ___    _ _    
    |  _|  / -_)  / _` |  | (__    / _ \  | ' \   
   _|_|_   \___|  \__,_|   \___|   \___/  |_||_|  
 _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
 "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
         @1337kid              v1.2
==================================================
''')
#
ua = UserAgent()
export_dir=os.getcwd()+'/export/'
#
def user_search(user,instance,header):
    res=requests.get(f'https://{instance}/api/v2/search?q={user}', headers=header)
    data=json.loads(res.text)
    for i in data['accounts']:
        if i['username']==user:return i
    else:
        print(f'{Fore.RED}[EXIT]{Fore.GREEN} No user with the username "@{user}" is present in {instance}')
        sys.exit()
def export_basic_info(info):
    prnt_info('User information')
    for i in info:
        if i in basic_data_fields:
            prnt_binfo(basic_data_fields[i],repr(info[i]))
    if os.path.exists(export_dir)==0:os.mkdir(export_dir)
    else:
        shutil.rmtree(export_dir)
        os.mkdir(export_dir)
    with open(f'{export_dir}basic.json','w') as f:
        json.dump(info,f,indent=4)
    prnt_info(f'User information exported to "{export_dir}basic.json"')
#=============================================
def EXIT():
    print(Style.RESET_ALL)
    sys.exit()
def HELP():
    print(f'''{Style.BRIGHT+Fore.GREEN}
    HELP
    ====

    Usage:
        fedicon [user@domain] [token file loc]
        fedicon example@pixelfed.com token.txt
    
    Username & Instance should be of the format "username@domain"''')
    EXIT()
def export_post(info):
    prnt_info(f' {info["id"]}','Status ID','  ')
    for i in info:
        if i in user_posts:
            prnt_binfo(user_posts[i],repr(info[i]),'  ')
    prnt_binfo('Media ID',repr(info['media_attachments'][0]['id']),'  ')
    prnt_binfo('Media URL',repr(info['media_attachments'][0]['url']),'  ')
    return info['media_attachments'][0]['id'],info['media_attachments'][0]['url']
def get_user_posts(id_,instance,header):
    print()
    prnt_info("Fetching recent Statuses/Posts")
    res=requests.get(f'https://{instance}/api/v1/accounts/{id_}/statuses', headers=header)
    data=json.loads(res.text)
    with open(f'{export_dir}statuses.json','w') as f:
        json.dump(data,f,indent=4)
    media_id=[]
    for i in data:
        mid=export_post(i)
        media_id.append(mid)
    prnt_info(f'"Statuses/Posts" data exported to "{export_dir}statuses.json"')
    print()
    a=input(f'{Fore.YELLOW}[----] {Fore.GREEN}Do you want to download the recent status images? (Y/N) : ')
    if a.lower()=='y':
        os.mkdir(export_dir+'posts/')
        for i in range(len(media_id)):
            res=requests.get(media_id[i][1], headers={"User-agent":ua.random})
            extension=mimetypes.guess_extension(res.headers['content-type'])
            with open(f'{export_dir}posts/{media_id[i][0]}{extension}','wb') as f:
                f.write(res.content)
            prnt_info(f'{i+1}/{len(media_id)} Downloaded','|',' ')
        prnt_info(f'Download images -> saved to {export_dir}posts/')
#=============================================
def pixelfedsearch(username):
    prnt_info(f'Searching for "@{username}"')
    prnt_info('Starting 30 threads...')
    instances=[['Status Code','Link']]
    domains=[]
    for i in open('/usr/share/fedcon/instances.txt'):
        domains.append(i.strip('\n'))
    def checkacc(domain):
        response = requests.get('https://'+domain+'/@'+username,timeout=3)
        return response.status_code
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url={executor.submit(checkacc, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_url):
            domain=future_to_url[future]
            try:
                data=future.result()
            except:pass
            else:
                instances.append([data,f'http://{domain}/@{username}'])
                if data==200:
                    print(f'  {Fore.YELLOW}[FOUND] {Fore.GREEN}{data}{Fore.WHITE} -> {Fore.BLUE}https://{domain}/@{username}')
    prnt_info('Finished')
    with open(f'{export_dir}UserSearch.csv','w',newline='') as f:
        fw=csv.writer(f)
        fw.writerows(instances)
    prnt_info(f'User Search data exported to {export_dir}UserSearch.csv')