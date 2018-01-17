import urllib.request
from PIL import Image

def check_img(url, name='data.jpg'):
    try:
        data = open(name,'wb')
        with urllib.request.urlopen(url) as f:
            data.write(f.read())
        data.close()
        img = Image.open(name)
        return True
    except OSError:
        return False
