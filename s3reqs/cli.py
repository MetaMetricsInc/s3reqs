import os
import shutil
from pip._internal import main as _main

import boto3
import click


s3 = boto3.client('s3')


class Deploy(object):

    config_path = 's3reqs.json'
    venv = '_venv'

    def __init__(self,requirements_file,bucket,zip_name):
        self.zip_name = zip_name
        self.requirements_file = requirements_file
        self.bucket = bucket

    def install_packages(self):
        """
        Install reqs to the self.venv or install an extension and
        it's reqs to the self.venv
        :return:
        """
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
        create a zip file, upload that zip file to S3
        :return:
        """
        self.create_package()
        #Upload the zip file to the specified bucket in the project config
        self.upload_zip()
        self.remove_zip_venv()

    def build_zip(self):
        shutil.make_archive(self.zip_name.replace('.zip',''),'zip',self.venv)

    def upload_zip(self):
        print('Uploading Zip {} to {} bucket.'.format(self.zip_name,
                                                      self.bucket))
        s3.upload_file(self.zip_name,self.bucket,self.zip_name)
        return self.bucket, self.zip_name


@click.group()
def s3reqs():
    pass


@s3reqs.command()
@click.argument('requirements_file')
@click.argument('bucket')
@click.argument('zip_name')
def publish(requirements_file,bucket,zip_name):
    Deploy(requirements_file,bucket,zip_name).publish()


@s3reqs.command()
@click.argument('zip_name')
def delete_reqs(zip_name):
    try:
        shutil.rmtree('/tmp/s3reqs/')

    except FileNotFoundError:
        pass
    try:
        os.remove('/tmp/{}'.format(zip_name))
    except FileNotFoundError:
        pass

if __name__ == '__main__':
    s3reqs()


