import urllib
import os

import unidecode as unidecode
from PIL import Image
import time
import requests
from slugify import slugify
import re
import unicodedata

from bs4 import BeautifulSoup
size2 = (450, 450)
width,height = '450', '450'
mainfolder = 'iphone-14'


# Making a GET request
r = requests.get('https://www.mobilesentrix.com/replacement-parts/apple/iphone-parts/'+mainfolder)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())
links = soup.find_all('a', {'class': 'product-image'})
def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height))
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')

def download_jpg(url, file_path, file_name):
    full_path = file_path + file_name + ".jpg"
    urllib.request.urlretrieve(url, full_path)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

for line in links:
    time.sleep(1)
    print(line['href'])

    imgurl = line.find('img',{'class':'small-img'})

    current_url = imgurl['data-original'].replace("/cache/1/small_image/210x/0dc2d03fe217f8c83829496872af24a0/", "/")
    folder_name = line['href'].replace("https://www.mobilesentrix.com/", "")+"_fonelink"
    #folder_name = line['alt'].replace("/","-")
    #folder_name = slugify(unidecode(folder_name))
    print(current_url)
    opener = urllib.request.build_opener()
    opener.addheader = hdr
    response = requests.get(current_url)

    if response.status_code:
        if os.path.exists(mainfolder) is False:
            os.mkdir(mainfolder)
        if os.path.exists(mainfolder) is False:
            os.mkdir(mainfolder)
        with open(os.path.join(mainfolder, folder_name+'.jpg'), 'wb') as fp:
            fp.write(response.content)
            fp.close()
            with Image.open(os.path.join(mainfolder, folder_name+'.jpg')) as im:
             im = resize(im,1000,1000)
             im.save(os.path.join(mainfolder, folder_name+'.jpg'))
