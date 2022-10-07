#!/usr/bin/python3
try:
    from sys import argv as param
    import re
    import os
    import uuid
    import requests
    import argparse

except Exception as err:
    print(err)

class Simple:
    def __init__(self, base_url):
        try:
            self.url    = str(base_url)
            self.res    = requests.get(self.url)
            self.status = self.res.status_code

        except Exception as err:
            print(err)

    def execute(self):
        try:
            def download_page_index(download_tool):
                download_page = "{}".format(download_tool)
                os.system(download_page)

            if self.status == 200:
                if os.path.exists('/usr/bin/wget'):
                    command = "wget {} -O se.html".format(self.url)
                    download_page_index(command)
            
                elif os.path.exists("/usr/bin/curl"):
                    command = "curl -o se.html {}".format(self.url)
                    download_page_index(command)
            
                else:
                    print("Please install wget or curl of continue ...")
                    
            
            else:
                print("[{}] it'not possible continue status code invalid".format(self.status))

            if self.status == 200: 
                result = open("se.html", "r")
            
                for x in result:
                    if re.search("contentUrl", x):
                        print()
                        result = "'{}'".format(x.split(":",1)[1].replace('"', '').replace(" ","")[:-2])
                    
                        print("\033[10;35m{}\033[0;m".format(result))

                        open_url     = "firefox --new-tab {}".format(result)
                        
                        if os.path.exists('/usr/bin/wget'):
                            download_url = "wget {} -O {}.mp4".format(result, uuid.uuid1())

                        elif os.path.exists('/usr/bin/curl'):
                            download_url = "curl -o {}.mp4 {}".format(uuid.uuid1(), result)

                        else:
                            print("Please in install wget or curl of continue ...")

                        download  = input("Deseja fazer o download do video?[y, n] ")
                        open_u    = input("Deseja abrir o link no navegador?[y, n] ")

                        if download == 'y':
                            os.system(download_url)
            
                        if open_u == 'y':
                            os.system(open_url)
        
                        os.system("rm se.html")
    
        except Exception as err:
            print(err)
    
if __name__ == '__main__':
    try:
        all = argparse.ArgumentParser(
                prog='main.py', 
                usage='python3 ./%(prog)s -u <base_url>', 
                description='Download of open video tool')

        all.add_argument('-u', help='base_url of the video', required=True)
        args = vars(all.parse_args())

        if args['u']:
            base_url = args['u']

            Simple = Simple(base_url)
            Simple.execute()
    
        else:
            print('Please add base_url of continue ...')

    except Exception as err:
        print(err)
                                                                                                        

