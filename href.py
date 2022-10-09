#!/usr/bin/python

from bs4 import BeautifulSoup
import re

def main():
    try:
        open_file = open('./page.html', 'r')
        soup = BeautifulSoup(open_file)
        result = soup.find_all('a')

        for x in result:
            node = str(x).split()[1]
            
            if node.__contains__("/video"):
                path_url = node.split('=')[1].replace('><img','')
                print(path_url)

    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
