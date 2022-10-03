#!/usr/bin/python3
try:
    import requests
    from sys import argv as param
    import re
    import os
    import uuid

except Exception as err:
    print(err)

def main(base_url):
    try:
        url           = str(base_url)
        download_page = "wget -nv {} -O se.html".format(url)
        os.system(download_page)

        r      = requests.get(url)
        status = r.status_code

        if status == 200: 
            result = open("se.html", "r")
            
            for x in result:
                if re.search("contentUrl", x):
                    print()
                    result = str(x).split(":",1)[1].replace('"', '')
                    
                    print("\033[10;35m{}\033[0;m".format(result))

            open_url     = "firefox --new-tab {}".format(result)
            download_url = "curl -o {}.mp4 {}".format(uuid.uuid1(), result)

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
    base_url = param[1]
    main(base_url)
