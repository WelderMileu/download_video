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
                clone_page = open("se.html", "r")
            
                for x in clone_page:
                    if re.search("contentUrl", x):
                        arrange    = x.split(":",1)[1].replace('"', '').replace(" ","")[:-2]
                        path_video = "{}".format(str(arrange))
                        
                        if args['vw']:
                            print("\n{}".format(colored(path_video, 'cyan')))

                        if args['o']:
                            if os.path.exists('/usr/bin/firefox'):
                                open_url = "firefox --new-tab '{}'".format(path_video)
                            
                            elif os.path.exists('/usr/bin/google-chrome'):
                                open_url = "google-chrome {}".format(path_video)        

                            elif os.path.exists('/usr/bin/goole'):
                                open_url = "google {}".format(path_video)

                            os.system(open_url)

                        if args['dl']:
                            print("\ndownloading video ...")
                            wget.download(path_video, '{}.mp4'.format(uuid.uuid1()))
                
                    if os.path.exists('./se.html'):
                        os.remove("./se.html")
    
        except Exception as err:
            print(err)
    
if __name__ == '__main__':
    try:
        all = argparse.ArgumentParser(
                prog='main.py', 
                usage='python3 ./%(prog)s -u <base_url> <params>', 
                description='video downloading tool')

        all.add_argument(
                '-u', 
                help='base_url of the video', 
                required=True)

        all.add_argument(
            '-dl',
            help='download of the video',
            action='store_true'
        )

        all.add_argument(
            '-vw',
            help='only view video url',
            action='store_true'
        )

        all.add_argument(
            '-o',
            help='open link in new browse',
            action='store_true'
        )

        args = vars(all.parse_args())

        if args['u']:
            base_url = args['u']

            Simple = Simple(base_url)
            Simple.execute()

    except Exception as err:
        print(err)
                         
                                                                                                        

