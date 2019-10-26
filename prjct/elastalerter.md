# ./elastalerter.py

## ENVIRONMENT:

<table>
<tr>
	<td><strong>ELASTICSEARCH</strong></td>
	<td><a href="https://www.elastic.co/downloads/past-releases/elasticsearch-7-4-0">v7.4.0</a></td>
</tr>
<tr>
	<td><strong>VIRTUAL ENVIRONMENT</strong></td>
	<td>Python 3.6</td>
</tr>
<tr>
	<td><strong>OPERATING SYSTEM</strong></td>
	<td>Linux (in this case: Ubuntu 18.04)</td>
</tr>
</table>

- This probably won't work on Windows.

---

## SET-UP

1. Download and run [elasticsearch 7.4.0](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz) for Linux.

   ```console
   $ tar xvf elasticsearch-7.4.0-linux-x86_64.tar.gz

     ...

   $ elasticsearch-7.4.0/bin/elasticsearch

     ...

   ```

2. Set-up a python virtual environment:

   ```console
   $ pip3 install virtualenv

   $ python3 -m virtualenv v_env

     Using base prefix '/usr'
     New python executable in <current working directory>/v_env/bin/python3
     Also creating executable in <current working directory>/v_env/bin/python
     Installing setuptools, pip, wheel...
     done.  

   $ source v_env/bin/activate

   (v_env) $
   ```

3. Download and install dependencies for __*elastalert.py*__

   ```console
   (v_env) $ pip install --requirement requirements.txt

     ...omitted...
     Installing collected packages: pytz, tzlocal, six, APScheduler, urllib3, idna, certifi, chardet, requests, 
     aws-requests-auth, blist, docutils, jmespath, python-dateutil, botocore, s3transfer, boto3, pycparser, cffi, 
     configparser, croniter, defusedxml, docopt, jsonschema, mock, PyStaticConfiguration, stomp.py, exotel, envparse, 
     python-magic, pbr, oauthlib, requests-oauthlib, requests-toolbelt, jira, PyYAML, PySocks, PyJWT, twilio, texttable, 
     elasticsearch, future, thehive4py, elastalert, tabulate
   
   (v_env) $ pip install .

     ...omitted...
     Successfully built elastalerter
     Installing collected packages: elastalerter
     Successfully installed elastalerter-0.0.1

   ```


