#!/usr/bin/python3
import requests
import os
from bs4 import BeautifulSoup
import re
import json

def main():
    try:
        url     = str(os.getenv('DOMAIN'))
        domain  = requests.get(url)
        code    = domain.status_code
        content = domain.text

        if code == 200: 
            soup = BeautifulSoup(content)
            f    = soup.find_all('script')

            schema = str(f[11])[89:-64].replace("'", '"')
            loads  = json.loads(schema)
                    
            px = ['240p', '320p', '480p', '720p', '1080p', '4k']
            px_c = []

            for t in loads:
                for p in px:
                    if p == t:
                        if len(loads[p]) > 0:
                            px_c.append(t)
                            print("[{}] {}".format(px.index(t), t))
                    
            opt = input('Escolha uma das opcoes de download: ')
            download = False

            for p in px_c:
                if px[int(opt)] == p:
                    download = True

            if download: 
                domain_s = loads[str(px[int(opt)])]
                domain_d = domain_s[0]
                content_length = requests.get(domain_d).headers['Content-Length']
                size = float(content_length) / 1024**2
                    
                print("Este video tem {:.2f}MB Deseja fazer o download?[y,n]".format(size))

            else:
                print("Opcao invalida")


        if os.path.exists('./se.html'):
            os.remove('./se.html')

    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
