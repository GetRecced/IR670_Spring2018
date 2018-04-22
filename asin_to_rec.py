import requests
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm

def create_request(asin_list):
    recommendations = ','.join([str(_) for _ in asin_list])
    url = "http://www.asinlab.com/php/convertfromasin.php?asin_num=" + recommendations + "&id_type=UPC&bulk=true&x=false"
    header = {}
    cookie = {}
    header["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    header["Accept-Encoding"] = "gzip, deflate"
    header["Accept-Language"] = "en-US,en;q=0.9"
    cookie["PHPSESSID"] = "7265269b431e4d9d9e4edd079f8da21c"
    cookie["sc_is_visitor_unique"] = "rx11430932.1524382929.F7A1330878D04FF9DF09539FE782C5B9.1.1.1.1.1.1.1.1.1"
    header["Referer"] = "http://www.asinlab.com/asin-to-upc-bulk-lookup/"
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
    return url, header, cookie

def get_recommendation_items(asin_list):

    url, header, cookie = create_request(asin_list)
    r = requests.get(url, headers=header, cookies=cookie)
    soup = BeautifulSoup(r.content, "lxml")
    urls = []
    imgs = []
    names = []
    for i in range(1):
        for tr in list(soup.find_all('tr'))[1:]:
            urls.append(list(tr.children)[0].find('img')['src'])
            img_response = requests.get(urls[-1])
            img = Image.open(StringIO(img_response.content))
            imgs.append(img)
            names.append(list(tr.children)[6].find('div').get_text())

        f, axarr = plt.subplots(1, len(imgs))

        for i in range(len(imgs)):
            axarr[i].imshow(imgs[i], cmap = cm.Greys_r)
            axarr[i].set_title(names[i])
            axarr[i].axis('off')
            f.tight_layout() 

        plt.show()