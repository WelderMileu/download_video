#!/usr/bin/python
try:
    from bs4 import BeautifulSoup
    import requests
    import re
    import json
    import uuid
    import wget
    from time import sleep
    import os
    import argparse

except Exception as err:
    print(err)

class Simple:
    def __init__(self, base_url):
        try:
            self.domain = str(base_url)
            self.res    = requests.get(self.domain)
            self.code   = self.res.status_code
            self.body   = self.res.text

            self.domain_categorie       = ""
            self.domain_download_video_and_thumb  = ""

            self.tmp_file_analysis = './se.html'
            self.tmp_file_image    = './image.jpg'

        except Exception as err:
            print(err)

    def list_categories(self):
        if self.code == 200:
            soup = BeautifulSoup(self.body)
            resp = soup.find_all("script")
                
            data   = str(resp[0])[52:-10]
            json_d = json.loads(data)
            categories_json = json_d['dyn']['categories']

            for x in categories_json:
                label = x['label']
                url   = x['url']

                domain_categorie  = "{}{}".format(self.domain, url)
                index_categorie   = categories_json.index(x)
                categorie_options = "[{}] {}".format(index_categorie, label)
                
                print(categorie_options)

            categorie_question = input("\nSelect index of only categorie: ")

            categorie_label    = categories_json[int(categorie_question)]['label']
            categorie_url      = categories_json[int(categorie_question)]['url']
            
            self.domain_categorie = "{}{}".format(self.domain, categorie_url)
                
            print(categorie_label)

    def list_videos(self):
        domain  = requests.get(self.domain_categorie)
        code    = domain.status_code
        content = domain.text 

        if code == 200:
            soup_v = BeautifulSoup(content)
            video_urls  = soup_v.find_all('a')
            content_url = [] 
            new_content_url =[]

            for c in video_urls:
                if str(c).__contains__('/video'):
                    path_video_url = str(c).split()[1].replace('><img', '')
                            
                    if str(path_video_url).__contains__('href'):
                        url_path   = str(path_video_url).split('=')[1].replace('"', '')
                        content_url.append(url_path)
            
            # no repeat path_video
            for i in content_url:
                if i not in new_content_url:
                    new_content_url.append(i)

            new_content_url.sort()
            
            for i in new_content_url:
                index_path = new_content_url.index(i)
                print("[{}] {}".format(index_path, i))
                           
            selected_path_video = input('\nSelect index of video: ')
            domain_u = new_content_url[int(selected_path_video)] 

            self.domain_download_video_and_thumb = "{}{}".format(self.domain, domain_u)

    def thumbnail_image_download(self, param):
        if re.search('"thumbnailUrl":', param):
            image_thumb = "{}".format(param.split()[1][1:-2]).replace('"', '')
                                
            quest = input("\nWant do download the image?[y,n] ")
                                
            if quest == 'y':
                wget.download(image_thumb, self.tmp_file_image)
                os.system('ristretto {} &'.format(self.tmp_file_image))

    def video_download(self, param):
        if re.search('"contentUrl":', param):
            domain_video = "{}".format(param.split()[1][1:-2])
            new_name = "{}.mp4".format(uuid.uuid1())

            quest_v = input("\nWant to download the video?[y,n]")
                                
            if quest_v == 'y':
                wget.download(domain_video, new_name)


    def download_file_analysis(self):
        domain = requests.get(self.domain_download_video_and_thumb)
        code   = domain.status_code
        resp   = domain.text

        wget.download(self.domain_download_video_and_thumb, self.tmp_file_analysis)

        if code == 200:
            read_file_analysis = open(self.tmp_file_analysis, 'r')
            
            for x in read_file_analysis:
                Simple.thumbnail_image_download(x)
                Simple.video_download(x)

    def remove_tmp_files(self):
        if os.path.exists(self.tmp_file_analysis):
            os.remove(self.tmp_file_analysis)
                        
        if os.path.exists(self.tmp_file_image):
            os.remove(self.tmp_file_image)

    def execute(self):
        try:
            Simple.list_categories()
            Simple.list_videos()
            Simple.download_file_analysis()
            Simple.remove_tmp_files()

        except Exception as err:
            print(err)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Download video',
            prog='tool.py',
            usage='python ./%(prog)s -u <base_url>'
            )

    parser.add_argument('-u', help="base url", required=True)
    opt = parser.parse_args()

    Simple = Simple(opt.u)
    Simple.execute()
                         
