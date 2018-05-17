#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests
from PIL import Image

try:
    from StringIO import StringIO as ioModule  # python2
except ImportError:
    from io import BytesIO as ioModule  # python 3

OUTPUT_DIRECTORY = 'data/'


def image_download(id, url):
    print("START: save {id} from {url}".format(id=id, url=url))
    file_name = os.path.join(OUTPUT_DIRECTORY, '{id}.jpg'.format(id=id))

    if os.path.exists(file_name):
        print("SKIPPED: Image {id} is already exists".format(id=id))
        return

    with requests.get(url) as response:
        image_data = response.content

    with Image.open(ioModule(image_data)) as pil:
        rgb = pil.convert('RGB')

    try:
        rgb.save(file_name, format='JPEG', quality=90)
    except Exception as e:
        print("WARNING: failed to save image, {}".format(str(e)))

    print("FINISHED: save {id} from {url}".format(id=id, url=url))


def read_json(file_path):
    with open(file_path, 'r') as f:
        dict_data = json.load(f)

    return dict_data


def main():
    print("1/2 Reading the train data...")
    train = read_json("data/train.json")
    print("keys: {}".format(train.keys()))
    print("2/2 Downloading the data...")

    for i in range(0, 10):
        if len(train['images'][i]['url']) > 1:
            print("INFO: Image URLs are prural")
            print(train['images'][i]['url'])

        image_download(train['images'][i]['image_id'], train['images'][i]['url'][0])


if __name__ == '__main__':
    main()
