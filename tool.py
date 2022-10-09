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

        except Exception as err:
            print(err)

    def execute(self):
        try:
            if self.code == 200:
                soup = BeautifulSoup(self.res.text)
                resp = soup.find_all("script")
                
                data   = str(resp[0])[52:-10]
                json_d = json.loads(data)

                categories = json_d['dyn']['categories']

                for x in categories:
                    label = x['label']
                    url   = x['url']
                    domain_categorie = "{}{}".format(self.domain, url)
                    index_c = categories.index(x)
                    options_categorie = "[{}] {}".format(index_c, label)
                
                    print(options_categorie)

                select_categorie = input("\nSelect only categorie: ")
                selected_categorie_label = categories[int(select_categorie)]['label']
                selected_categorie_url   = categories[int(select_categorie)]['url']
                domain_categorie = "{}{}".format(self.domain, selected_categorie_url)
                
                print(selected_categorie_label)
                
                r       = requests.get(domain_categorie)
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
                            
                    selec_path_video = input('\nSelect index of video: ')
                    domain_u = str(video_urls[int(selec_path_video)]).split()[1].replace('"', '').replace("href=", "")

                    domain_download = "{}{}".format(self.domain, domain_u)
                    
                    sleep(3)

                    d_r = requests.get(domain_download)
                    d_s = d_r.status_code
                    d_t = d_r.text

                    if d_s == 200:
                        wget.download(domain_download, './se.html')
                        
                        path_page = open('./se.html', 'r')

                        for t in path_page:
                            if re.search('"thumbnailUrl":', t):
                                image_thumb = "{}".format(t.split()[1][1:-2]).replace('"', '')
                                
                                quest = input("Deseja fazer o download?[y,n] ")
                                
                                if quest == 'y':
                                    wget.download(image_thumb, 'image.jpg')
                                    os.system('ristretto ./image.jpg &')
                                
                            
                            if re.search('"contentUrl":', t):
                                domain_video = "{}".format(t.split()[1][1:-2])
                                new_name = "{}.mp4".format(uuid.uuid1())

                                quest_v = input("Deseja fazer o download do video?[y,n]")
                                
                                if quest_v == 'y':
                                    wget.download(domain_video, new_name)

                        os.remove('./se.html')
                        
                        if os.path.exists('./image.jpg'):
                            os.remove('./image.jpg')
            else:
                print('domain not found')

        except Exception as err:
            print(err)

if __name__ == '__main__':
    Simple = Simple()
    Simple.execute()
