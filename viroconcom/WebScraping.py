
import requests
from bs4 import BeautifulSoup

URL = "https://apps.ecmwf.int/datasets/data/interim-full-daily/levtype=sfc/"

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

