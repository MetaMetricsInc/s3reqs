# s3reqs
Uploads zip file to S3 of requirements for Python AWS Lambda apps to get around 50MB limit.

## Wait what?
**From AWS' developer guide for AWS Lambda:** "Each Execution Context provides 500MB of additional disk space in the /tmp directory. The directory content remains when the Execution Context is frozen, providing transient cache that can be used for multiple invocations. You can add extra code to check if the cache has the data that you stored. For information on deployment limits, see AWS Lambda Limits."
## Install

```bash
pip install s3reqs
```
## Command Line Interface

### Publish

```bash
>>> s3reqs publish s3_reqs.txt your-bucket your-reqs.zip
Collecting numpy (from -r s3_reqs.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/fe/94/7049fed8373c52839c8cde619acaf2c9b83082b935e5aa8c0fa27a4a8bcc/numpy-1.15.1-cp36-cp36m-manylinux1_x86_64.whl
Collecting scipy (from -r s3_reqs.txt (line 2))
  Using cached https://files.pythonhosted.org/packages/a8/0b/f163da98d3a01b3e0ef1cab8dd2123c34aee2bafbb1c5bffa354cc8a1730/scipy-1.1.0-cp36-cp36m-manylinux1_x86_64.whl
Collecting seaborn (from -r s3_reqs.txt (line 3))
  Using cached https://files.pythonhosted.org/packages/a8/76/220ba4420459d9c4c9c9587c6ce607bf56c25b3d3d2de62056efe482dadc/seaborn-0.9.0-py3-none-any.whl
Collecting matplotlib (from -r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/9e/59/f235ab21bbe7b7c6570c4abf17ffb893071f4fa3b9cf557b09b60359ad9a/matplotlib-2.2.3-cp36-cp36m-manylinux1_x86_64.whl
Collecting pandas>=0.15.2 (from seaborn->-r s3_reqs.txt (line 3))
  Using cached https://files.pythonhosted.org/packages/e1/d8/feeb346d41f181e83fba45224ab14a8d8af019b48af742e047f3845d8cff/pandas-0.23.4-cp36-cp36m-manylinux1_x86_64.whl
Collecting pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.1 (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/6a/8a/718fd7d3458f9fab8e67186b00abdd345b639976bc7fb3ae722e1b026a50/pyparsing-2.2.0-py2.py3-none-any.whl
Collecting cycler>=0.10 (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/f7/d2/e07d3ebb2bd7af696440ce7e754c59dd546ffe1bbe732c8ab68b9c834e61/cycler-0.10.0-py2.py3-none-any.whl
Collecting kiwisolver>=1.0.1 (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/69/a7/88719d132b18300b4369fbffa741841cfd36d1e637e1990f27929945b538/kiwisolver-1.0.1-cp36-cp36m-manylinux1_x86_64.whl
Collecting pytz (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/30/4e/27c34b62430286c6d59177a0842ed90dc789ce5d1ed740887653b898779a/pytz-2018.5-py2.py3-none-any.whl
Collecting python-dateutil>=2.1 (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/cf/f5/af2b09c957ace60dcfac112b669c45c8c97e32f94aa8b56da4c6d1682825/python_dateutil-2.7.3-py2.py3-none-any.whl
Collecting six>=1.10 (from matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl
Collecting setuptools (from kiwisolver>=1.0.1->matplotlib->-r s3_reqs.txt (line 4))
  Using cached https://files.pythonhosted.org/packages/66/e8/570bb5ca88a8bcd2a1db9c6246bb66615750663ffaaeada95b04ffe74e12/setuptools-40.2.0-py2.py3-none-any.whl
Installing collected packages: numpy, scipy, pyparsing, six, cycler, setuptools, kiwisolver, pytz, python-dateutil, matplotlib, pandas, seaborn
Successfully installed cycler-0.10.0 kiwisolver-1.0.1 matplotlib-2.2.3 numpy-1.15.1 pandas-0.23.4 pyparsing-2.2.0 python-dateutil-2.7.3 pytz-2018.5 scipy-1.1.0 seaborn-0.9.0 setuptools-40.2.0 six-1.11.0
Uploading Zip your-reqs.zip to your-bucket bucket.
```

## Download Packages Decorator
This decorator downloads the packages if and only if packages zip file is not present 
in the **/tmp/** folder and adds to the **PYTHONPATH**.

**IMPORTANT:** Although the example shown below uses AWS' Chalice framework this will work with any function.
```python
from chalice import Chalice
from s3reqs.utils import download_packages


app = Chalice(app_name="helloworld")

#In a real app you should probably use environment variables for the  
#bucket and req_key arguments
@download_packages('your-bucket','your-reqs.zip')
@app.route("/")
def index():
    return {"hello": "world"}
```
