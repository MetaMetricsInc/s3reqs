from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name='s3reqs',
    description='Uploads zip file to S3 of requirements for Python AWS Lambda '
                'apps to get around 50MB limit.',
    url='https://github.com/metametricsinc/s3reqs',
    author='Brian Jinwright',
    license='GNU GPL v3',
    keywords='requirements, lambda',
    install_requires=parse_requirements('requirements.txt'),
    packages=find_packages(),
    include_package_data=True,
    version='0.3.0a',
    entry_points='''
        [console_scripts]
        s3reqs=s3reqs.cli:s3reqs
        ''',
)
