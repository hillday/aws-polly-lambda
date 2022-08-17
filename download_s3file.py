#!/usr/bin/python3

import time
import sys
import os
import boto3
from datetime import datetime
import pytz



if len(sys.argv) < 5:
    print("params is error,usage: python download_s3file.py [bucket] [key] [start_time] [end_time]")
    print('python download_s3file.py mytest test/source/ "2022-08-16 00:00:00" "2022-08-18 00:00:00"')
    exit(-1)

g_video_source_s3_bucket = sys.argv[1]
g_video_source_s3_prefix = sys.argv[2]
g_from_time = sys.argv[3]
g_format = "%Y-%m-%d %H:%M:%S"
g_end_time = sys.argv[4]

s3 = boto3.resource('s3') # assumes credentials & configuration are handled outside python in .aws directory or environment variables

def check_object_download(bucket_name,key):
    object = s3.Object(bucket_name, key)
    from_date = datetime.strptime(g_from_time, g_format)
    

    if g_end_time is None:
        to_date = datetime.now()
    else:
        to_date = datetime.strptime(g_end_time, g_format)

    from_date = from_date.replace(tzinfo=pytz.timezone('UTC'))
    to_date = to_date.replace(tzinfo=pytz.timezone('UTC'))
    if object.last_modified >= from_date and object.last_modified <= to_date:
        return True
    else:
        return False

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        if check_object_download(bucket_name, obj.key) == True:
            print(f"donwload file {obj.key}")
            bucket.download_file(obj.key, target)


if(__name__ == "__main__"):
    download_s3_folder(g_video_source_s3_bucket,g_video_source_s3_prefix)
