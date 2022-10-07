#!/usr/bin/python3
try:
    from sys import argv as param
    import re
    import os
    import uuid
    import requests
    import argparse
    import wget
    from termcolor import colored

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
            if self.status == 200:
                wget.download(self.url, './se.html')    

            if self.status == 200: 
                result = open("se.html", "r")
            
                for x in result:
                    if re.search("contentUrl", x):
                        print()
                        repl   = x.split(":",1)[1].replace('"', '').replace(" ","")[:-2]
                        result = "{}".format(str(repl))

                        print("\n{}".format(colored(result, 'cyan')))

                        open_url     = "firefox --new-tab {}".format(result)
            
                        download  = input("\nDeseja fazer o download do video?[y, n] ")
                        open_u    = input("Deseja abrir o link no navegador?[y, n] ")

                        if download == 'y':
                            print("\nDownload of the video.")
                            wget.download(result, '{}.mp4'.format(uuid.uuid1()))
            
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

    except Exception as err:
        print(err)
                         
