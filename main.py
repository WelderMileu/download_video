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
    print("exports: ", err)

class Simple:
    def __init__(self, base_url):
        try:
            self.url         = str(base_url)
            self.res         = requests.get(self.url)
            self.status      = self.res.status_code
            self.page_clone  = "./se.html"
            self.path_video  = ""

        except Exception as err:
            print(err)

    def clone_page(self):
        if self.status == 200: 
            wget.download(self.url, self.page_clone)     


    def get_contentUrl(self):
        contentUrl = open(self.page_clone, 'r')

        for x in contentUrl:
            if re.search("contentUrl", x):
                arrange    = x.split(":",1)[1].replace('"', '').replace(" ","")[:-2]
                self.path_video = "{}".format(str(arrange))


    def show_url(self):
        if args['vw']:
            print("\n{}".format(colored(self.path_video, 'cyan')))

    def open_browse(self):
        if args['o']:
            if os.path.exists('/usr/bin/firefox'):
                open_url = "firefox --new-tab '{}'".format(self.path_video)

            elif os.path.exists('/usr/bin/google-chrome'):
                open_url = "google-chrome {}".format(self.path_video)

            elif os.path.exists('/usr/bin/goole'):
                open_url = "google {}".format(self.path_video)

            os.system(open_url)

    def download_video(self):
        if args['dl']:
            print("\ndownloading video ...")
            wget.download(self.path_video, '{}.mp4'.format(uuid.uuid1()))
    
    def remove_page_clone(self):            
        if os.path.exists(self.page_clone):
            os.remove(self.page_clone)

    def main(self):
        Simple.clone_page()
        Simple.get_contentUrl()
        Simple.show_url()
        Simple.open_browse()
        Simple.download_video()
        Simple.remove_page_clone()

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
            Simple.main()

    except Exception as err:
        print(err)
                         
                                                                                                        

                                                 
