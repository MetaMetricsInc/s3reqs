import os
import shutil
from pip._internal import main as _main

import boto3
import click
import json


s3 = boto3.client('s3')


class Deploy(object):

    config_path = 's3reqs.json'
    venv = '_venv'

    def __init__(self):
        config = self.parse_config()
        self.zip_name = config.get('zip_name')
        self.requirements_file = config.get('requirements_file')
        self.bucket = config.get('bucket')

    def parse_config(self):
        with open(self.config_path, 'r') as f:
            c = json.load(f)
        return c

    def install_packages(self):
        """
        Install reqs to the self.venv or install an extension and
        it's reqs to the self.venv
        :return:
        """
        #If there is no extension name we can assume we are installing loadlamb's requirements
        _main(['install','-r',self.requirements_file,'-t',self.venv])

    def remove_zip_venv(self):
        self.remove_venv()

    def remove_zip(self):
        os.remove(self.zip_name)

    def remove_venv(self):
        shutil.rmtree(self.venv)

    def create_package(self):
        self.install_packages()
        # Install reqs to the self.venv folder
        # Zip the self.venv folder
        self.build_zip()

    def publish(self):
        """
        Runs all of the methods required to build the virtualenv folder,
        create a zip file, upload that zip file to S3, create a SAM
        template, and deploy that SAM template.
        :return:
        """
        self.create_package()
        #Upload the zip file to the specified bucket in the project config
        self.upload_zip()
        self.remove_zip_venv()

    def build_zip(self):
        shutil.make_archive(self.zip_name.replace('.zip',''),'zip',self.venv)

    def upload_zip(self):
        print('Uploading Zip {} to {} bucket.'.format(self.zip_name,self.bucket))
        s3.upload_file(self.zip_name,self.bucket,self.zip_name)
        return self.bucket, self.zip_name


@click.group()
def s3reqs():
    pass


@s3reqs.command()
@click.option('--requirement-file',prompt=True)
@click.option('--bucket',prompt=True)
@click.option('--zip-name',prompt=True)
def init(requirement_file,bucket,zip_name):
    with open('s3reqs.json','w+') as f:
        f.write(json.dumps(dict(requirement_file=requirement_file,bucket=bucket,
                  zip_name=zip_name)))

@s3reqs.command()
def publish():
    Deploy().publish()


if __name__ == '__main__':
    s3reqs()


