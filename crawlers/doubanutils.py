# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-16 13:40:26
# @Last Modified by:   mcxiaoke
from __future__ import print_function
import codecs
import requests
import base64
import json
import sys
import os
import time
import shutil
import random
import argparse
import traceback
from utils import read_list, write_list
from doubanapi import ApiClient

api = ApiClient()


def upload_photos_to_album(album_id, photos):
    print('Upload photos to album %s' % album_id)
    if os.path.isfile(photos):
        files = [os.path.basename(photos)]
        output = os.path.dirname(photos)
    else:
        files = os.listdir(photos)
        output = photos
    done_file = os.path.join(output, '%s_done.txt' % album_id)
    finished = read_list(done_file)
    error_count = 0
    for f in files:
        image = os.path.join(output, f)
        _, ext = os.path.splitext(f)
        if not ext or ext.lower() not in ['.jpg', '.png', '.gif']:
            # print('Invalid %s' % image)
            continue
        try:
            if f not in finished:
                print('Uploading %s' % image)
                api.photo_upload(album_id, image, f)
                finished.append(f)
                write_list(done_file, finished)
                time.sleep(random.randint(1, 3))
            else:
                print('Skip %s' % image)
        except KeyboardInterrupt, e:
            print("User interrupt, quit.")
            raise
        except Exception, e:
            print("Error:%s On uploading :%s" % (e, image))
            traceback.print_exc()
            error_count += 1
            if error_count > 5:
                break
            time.sleep(error_count * 10)
    write_list(done_file, finished)
