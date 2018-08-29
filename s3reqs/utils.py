import boto3
import os
import sys
import zipfile

from envs import env

s3 = boto3.client('s3')


def download_packages(bucket=None,req_key=None):
    LOCAL_ENV = env('LOCAL_ENV',True,var_type='boolean')
    if LOCAL_ENV != True:
        tmp_folder = '/tmp/s3reqs/'
        tmp_file = '/tmp/{}'.format(req_key)
        file_exists = os.path.isfile(tmp_file)
        if not file_exists:
            s3.download_file(bucket, req_key, tmp_file)
            with zipfile.ZipFile(tmp_file,'r') as zip_ref:
                zip_ref.extractall(tmp_folder)
            sys.path.insert(0,tmp_folder)

