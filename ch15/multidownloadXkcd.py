#! python3
# multidownloadXkcd.py - Downloads XKCD comics using multiple threads.

import os
import threading
import urllib.parse

import bs4
import requests


os.makedirs('xkcd', exist_ok=True)  # store comics in ./xkcd


def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        # Download the page.
        print(f'Downloading page http://xkcd.com/{urlNumber}...')
        res = requests.get(f'http://xkcd.com/{urlNumber}')
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        # Find the URL of the comic image.
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin
            comicUrl = urllib.parse.urljoin(
                'http://xkcd.com/', comicElem[0].get('src'))

            # Download the image.
            print(f'Downloading image {comicUrl}...')
            res = requests.get(comicUrl)
            res.raise_for_status()

            # Save the image to ./xkcd
            imageFile = open(os.path.join(
                'xkcd', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()


# Create and start the Thread objects.
downloadThreads = []  # a list of all the Thread objects
for i in range(1, 1400, 100):  # loops 14 times, creates 14 threads
    downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))
    downloadThreads.append(downloadThread)
    downloadThread.start()

# Wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')
