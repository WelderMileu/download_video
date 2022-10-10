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

except Exception as err:
    print(err)

class Simple:
    def __init__(self):
        try:
            self.domain = '<base_url>'
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
        r       = requests.get(self.domain_categorie)
        code    = r.status_code
        content = r.text 

        if code == 200:
            soup_v = BeautifulSoup(content)
            video_urls = soup_v.find_all('a')
                    
            for c in video_urls:
                if str(c).__contains__('/video'):
                    path_video_url = str(c).split()[1].replace('><img', '')
                            
                    if str(path_video_url).__contains__('href'):
                        url_path   = str(path_video_url).split('=')[1].replace('"', '')
                        index_path = video_urls.index(c)
                                
                        print("[{}] {}".format(index_path, url_path))
                            
            selected_path_video = input('\nSelect index of video: ')
            domain_u = str(video_urls[int(selected_path_video)]).split()[1].replace('"', '').replace("href=", "")

            self.domain_download_video_and_thumb = "{}{}".format(self.domain, domain_u)

    def thumbnail_image_download(self, param):
        if re.search('"thumbnailUrl":', param):
            image_thumb = "{}".format(param.split()[1][1:-2]).replace('"', '')
                                
            quest = input("Deseja fazer o download?[y,n] ")
                                
            if quest == 'y':
                wget.download(image_thumb, 'image.jpg')
                os.system('ristretto ./image.jpg &')

    def video_download(self, param):
        if re.search('"contentUrl":', param):
            domain_video = "{}".format(param.split()[1][1:-2])
            new_name = "{}.mp4".format(uuid.uuid1())

            quest_v = input("Deseja fazer o download do video?[y,n]")
                                
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

    def remove_temp_files(self):
        if os.path.exists(self.tmp_file_analysis):
            os.remove(self.tmp_file_analysis)
                        
        if os.path.exists(self.tmp_file_image):
            os.remove(self.tmp_file_image)

    def execute(self):
        try:
            Simple.list_categories()
            Simple.list_videos()
            Simple.download_file_analysis()
            Simple.remove_temp_files()

        except Exception as err:
            print(err)

if __name__ == '__main__':
    Simple = Simple()
    Simple.execute()
