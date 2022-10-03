#!/usr/bin/python3
try:
    from sys import argv as param
    import re, os, uuid, requests

except Exception as err:
    print(err)

class Simple(base_url):
    def __init__(self):
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
                    command = "wget -nv {} -O man.html".format(self.url)
                    download_page_index(command)
            
                elif os.path.exists("/usr/bin/curl"):
                    command = "curl -o man.html {}".format(self.url)
                    download_page_index(command)
            
                else:
                    print("Please install wget or curl of continue ...")
                    break
            
            else:
                print("[{}] it'not possible continue status code invalid".format(self.status))
                break

        if status == 200: 
            result = open("se.html", "r")
            
            for x in result:
                if re.search("contentUrl", x):
                    print()
                    result = "'{}'".format(x.split(":",1)[1].replace('"', '').replace(" ","")[:-2])
                    
                    # result = str(x).split(":", 1)[1][:-2].replace('"',"").replace(" ", "").replace("\n", "").split()[0]
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
