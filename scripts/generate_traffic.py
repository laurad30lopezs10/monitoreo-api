import requests
import time

urls = [
    "http://localhost:3000/",
    "http://localhost:3000/api/datos",
    "http://localhost:3000/api/lento"
]

while True:
    for url in urls:
        try:
            requests.get(url)
        except:
            pass
    time.sleep(1)