#!/usr/bin/python3
try:
    import requests
    import os
    import re
    import json
    import wget
    import uuid
    import argparse

except Exception as err:
    print(err)

class Simple:
    def __init__(self, base_url):
        try:
            self.url     = str(base_url)
            self.domain  = requests.get(self.url)
            self.code    = self.domain.status_code
            self.content = self.domain.text

            self.anality_f = './se.html'
            self.px = ['240p', '320p', '480p', '720p', '1080p', '4k']
            self.px_c = []

            self.download = False
            self.loads    = ''
            self.opt = ''

        except Exception as err:
            print(err)

    def download_file_anality(self):
        if self.code == 200:
            payload = "wget -nv {} -O {}".format(self.url, self.anality_f)
            os.system(payload)


    def generate_data(self):
        anality_f = open(self.anality_f, 'r')
        
        for x in anality_f:
            if re.search("var stream_data = ", x):
                json_d = x[22:-2].replace("'", '"')
                self.loads = json.loads(json_d)

    def list_opts_px(self):
        for t in self.loads:
            for p in self.px:
                if p == t:
                    if len(self.loads[p]) > 0:
                        self.px_c.append(t)
                        print("[{}] {}".format(self.px.index(t), t))

        self.opt = input('Escolha uma das opcoes de download: ')

    def validade_download(self):
        for p in self.px_c:
            if self.px[int(self.opt)] == p:
                self.download = True

    def download_video(self):
        if self.download: 
            domain_s = self.loads[str(self.px[int(self.opt)])]
            domain_d = domain_s[0]

            content_length = requests.get(domain_d).headers['Content-Length']
            size = float(content_length) / 1024**2

            q = input("Este video tem {:.2f}MB Deseja fazer o download?[y,n] ".format(size))
                    
            if q == 'y':
                wget.download(domain_d, "{}.mp4".format(uuid.uuid1()))                    
            else:
                print("Opcao invalida")

    def remove_tmp(self):
        if os.path.exists(self.anality_f):
            os.remove(self.anality_f)

    def main(self):
            try:
        
                Simple.download_file_anality()
                Simple.generate_data()
                Simple.list_opts_px()
                Simple.validade_download()
                Simple.download_video()
                Simple.remove_tmp()

            except Exception as err:
                print(err)

if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(
            description='Download video',
            prog='sb.py',
            usage='python3 %(prog)s -u <base_url>'
        )

        args.add_argument('-u', help='base_url of domain', required=True)
        var = vars(args.parse_args())

        Simple = Simple(var['u'])
        Simple.main()
        
    except Exception as err:
        print(err)       
