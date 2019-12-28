---
layout: menu
title: "elastalerter.py"
description: "An elastalert rule tester using python."
tags: [elastalert, elasticsearch, rule, rules, test, aggregation]
---

# <span style="color:red">./elastalerter.py</span>

---

## ENVIRONMENT

<div style="overflow-x:auto"><table>
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
</table></div>

---

## IMPORTANT NOTES

- This probably <span style="color:red">__won't work__</span> on Windows Machines.
- The program manually creates a basic config file if none is specified.
- The program manually sets the rule's alert to __`elastalerter.alerter.Alert`__.
- If mappings are not specified during aggregation, key fields are __automatically set as keyword fields__:
  ```yaml
  query_key: field_name.keyword
  metric_agg_key: field_name.keyword
  ```
- Logs to be used in a specific test could be a list of files or a directory containing all logs to be indexed.
  ```json
  "log": ["log1.json", "log2.json", ...]
  
   or

  "log": "/dir"
  ```
- If a directory is specified, the program will check if it exists as is, in the directory specified in __`--logs`__, or in the current working directory.
- Test results are laid out as follows in __`results.json`__:
  ```json
  {
      "total": 6,
      "pass": 3,
      "fail": 3,
      "tests": {
          "test_2": {
              "result": "PASSED",
              "message": []
          },
          "test_2": {
              "result": "PASSED",
              "message": []
          },
          "test_3": {
              "result": "FAILED",
              "message": [
                  "1 LOG(S) MATCHED: log001.json"
              ]
          },
          "test_4": {
              "result": "FAILED",
              "message": [
                  "7 LOG(S) DID NOT MATCH: agg_log001.json, agg_log002.json, agg_log003.json, agg_log004.json, agg_log005.json, log001.json, log003.json"
              ]
          },
          "test_agg_1": {
              "result": "FAILED",
              "message": [
                  "HITS (5) EXCEEDED THE THRESHOLD"
              ]
          }
      }
  }
  ```

---

## SET-UP

1. Download and run [elasticsearch 7.4.0](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz) for Linux.

   ```shell
   $ tar xvf elasticsearch-7.4.0-linux-x86_64.tar.gz

     ...

   $ elasticsearch-7.4.0/bin/elasticsearch

     ...

   ```

2. Set-up a python virtual environment:

   ```shell
   $ pip3 install virtualenv

   $ python3 -m virtualenv v_env

     Using base prefix '/usr'
     New python executable in CURRENT_WORKING_DIRECTORY/v_env/bin/python3
     Also creating executable in CURRENT_WORKING_DIRECTORY/v_env/bin/python
     Installing setuptools, pip, wheel...
     done.

   $ source v_env/bin/activate

   (v_env) $
   ```

3. Download and install dependencies for __*elastalerter.py*__

   ### download and unzip the files
   ```shell
   (v_env) $ wget https://github.com/jebidiah-anthony/elastalerter/blob/master/elastalerter.zip?raw=true
   
     ...omitted...
     HTTP request sent, awaiting response... 200 OK
     Length: 4248 (4.1K) [application/zip]
     Saving to: ‘elastalerter.zip’

     elastalerter.zip         100%[================================>]   4.15K  --.-KB/s    in 0s
     ...omitted...
   
   (v_env) $ unzip elastalerter.py 
   
     Archive:  elastalerter.zip
       inflating: elastalerter.py
       inflating: requirements.txt
       inflating: setup.py 

   ```

   ### install dependencies
   ```shell
   (v_env) $ pip install --requirement requirements.txt
   
     ...omitted...
     Installing collected packages: pytz, tzlocal, six, APScheduler, urllib3, idna, certifi, chardet, requests, 
     aws-requests-auth, blist, docutils, jmespath, python-dateutil, botocore, s3transfer, boto3, pycparser, cffi, 
     configparser, croniter, defusedxml, docopt, jsonschema, mock, PyStaticConfiguration, stomp.py, exotel, 
     envparse, python-magic, pbr, oauthlib, requests-oauthlib, requests-toolbelt, jira, PyYAML, PySocks, PyJWT, 
     twilio, texttable, elasticsearch, future, thehive4py, elastalert, tabulate
     ...omitted...

   ```

   ### install the alerter
   ```shell
   (v_env) $ pip install .
   
     ...omitted...
     Successfully built elastalerter
     Installing collected packages: elastalerter
     Successfully installed elastalerter-0.0.2

   ```

---

## EXECUTION (w/ sample output)

### help (__`-h, --help`__)
```shell
(v_env) $ python elastalerter.py -h
```
```
usage: python ./elastalerter.py --logs LOGS_DIR --rules RULES_DIR --expected expected.json

    SAMPLE "expected.json"
    ------------------------------------------------
    {
        "test_1": {
            "rule": "rule.yaml",
            "log": ["log1.json", "log2.json", ...],
            "match": (true | false),
            "enabled": (true | false)
        },
        "test_2": {
            ...
            "log": "/dir"
            ...
        },
        ...
    }

optional arguments:
  -h, --help       show this help message and exit
  --host HOST      elasticsearch instance host address (default: 127.0.0.1)
  --port PORT      elasticsearch instance port (default: 9200)
  --config YAML    elastalert config file to use.
  --mappings JSON  field data type mappings.
  --verbose        output other details

required arguments:
  --expected JSON  JSON outline of test names and expected results
  --logs DIR       directory of the logs to be indexed
  --rules DIR      directory of the rules to run with elastalert
```

### default output
```shell
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected expected.json
```
<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span style="color:#779ECB">[+] RUNNING test_1 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    <span style="color:green">[+] TEST ( test_1 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_2 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    <span style="color:green">[+] TEST ( test_2 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_3 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    <span style="color:red">[+] TEST ( test_3 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_4 :</span>
    <span style="color:orange">[+] SPECIFIED LOGS IS A DIRECTORY ( ./logs )</span>
        <span style="color:red">[ERROR] "test_file" IS NOT A VALID JSON FILE.</span>
        <span style="color:red">[ERROR] "test_file.json" IS NOT A VALID LOG FILE.</span>
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    <span style="color:red">[+] TEST ( test_4 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_1 :</span>
    <span style="color:orange">[+] TESTING RULE -- AGG_RULE01 ( ./agg_rule01.yaml )</span>
    <span style="color:red">[+] TEST ( test_agg_1 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_02 :</span>
    <span style="color:orange">[+] TEST ( test_agg_2 ) WAS DISABLED</span>


<span style="color:orange">[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json</span>


    ╒════════════╤══════════╤═════════════════════════════════════════════════════════════╕
    │ TestID     │ RESULT   │ MESSAGE                                                     │
    ╞════════════╪══════════╪═════════════════════════════════════════════════════════════╡
    │ test_1     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_2     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_3     │ FAILED   │ &gt; 1 LOG(S) MATCHED: log001.json                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_4     │ FAILED   │ &gt; 7 LOG(S) DID NOT MATCH: agg_log001.json, agg_log002.json, │
    │            │          │   agg_log003.json, agg_log004.json, agg_log005.json,        │
    │            │          │   log001.json, log003.json                                  │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_agg_1 │ FAILED   │ &gt; HITS (5) EXCEEDED THE THRESHOLD                           │
    ╘════════════╧══════════╧═════════════════════════════════════════════════════════════╛
</code></pre></div></div>

### mappings (__`--mappings`__)

#### > sample mappings.json
```json
{
    "mappings": {
        "properties": {
            "ip": { "type": "ip" },
            "port": { "type": "integer" }
        }
    }
}
```

#### > execution
```shell
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected expected.json --mappings mappings.json
```
<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span style="color:#779ECB">[+] RUNNING test_1 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    <span style="color:green">[+] TEST ( test_1 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_2 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    <span style="color:green">[+] TEST ( test_2 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_3 :</span>
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    <span style="color:red">[+] TEST ( test_3 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_4 :</span>
    <span style="color:orange">[+] SPECIFIED LOGS IS A DIRECTORY ( ./logs )</span>
        <span style="color:red">[ERROR] "test_file" IS NOT A VALID JSON FILE.</span>
        <span style="color:red">[ERROR] "test_file.json" IS NOT A VALID LOG FILE.</span>
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    <span style="color:red">[+] TEST ( test_4 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_1 :</span>
    <span style="color:orange">[+] TESTING RULE -- AGG_RULE01 ( ./agg_rule01.yaml )</span>
    <span style="color:red">[+] TEST ( test_agg_1 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_02 :</span>
    <span style="color:orange">[+] TEST ( test_agg_2 ) WAS DISABLED</span>


<span style="color:orange">[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json</span>


    ╒════════════╤══════════╤═════════════════════════════════════════════════════════════╕
    │ TestID     │ RESULT   │ MESSAGE                                                     │
    ╞════════════╪══════════╪═════════════════════════════════════════════════════════════╡
    │ test_1     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_2     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_3     │ FAILED   │ &gt; 1 LOG(S) MATCHED: log001.json                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_4     │ FAILED   │ &gt; 7 LOG(S) DID NOT MATCH: agg_log001.json, agg_log002.json, │
    │            │          │   agg_log003.json, agg_log004.json, agg_log005.json,        │
    │            │          │   log001.json, log003.json                                  │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_agg_1 │ FAILED   │ &gt; HITS (5) EXCEEDED THE THRESHOLD                           │
    ╘════════════╧══════════╧═════════════════════════════════════════════════════════════╛
</code></pre></div></div>

### verbose (__`--verbose`__)
```shell
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json --verbose
```
<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span style="color:#779ECB">[+] RUNNING test_1 :</span>
    [+] A NEW INDEX ( test_1 ) WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    [+] UPDATING RESULTS...
    [+] DELETING TEST INDEX...
    <span style="color:green">[+] TEST ( test_1 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_2 :</span>
    [+] A NEW INDEX ( test_2 ) WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    [+] UPDATING RESULTS...
    [+] DELETING TEST INDEX...
    <span style="color:green">[+] TEST ( test_2 ) PASSED</span>

<span style="color:#779ECB">[+] RUNNING test_3 :</span>
    [+] A NEW INDEX ( test_3 ) WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    <span style="color:orange">[+] TESTING RULE -- RULE01 ( ./rule01.yaml )</span>
    [+] UPDATING RESULTS...
    [+] DELETING TEST INDEX...
    <span style="color:red">[+] TEST ( test_3 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_4 :</span>
    [+] A NEW INDEX ( test_4 ) WAS CREATED
    <span style="color:orange">[+] SPECIFIED LOGS IS A DIRECTORY ( ./logs )</span>
        <span style="color:red">[ERROR] "test_file" IS NOT A VALID JSON FILE.</span>
        <span style="color:red">[ERROR] "test_file.json" IS NOT A VALID LOG FILE.</span>
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    <span style="color:orange">[+] TESTING RULE -- RULE02 ( ./rule02.yaml )</span>
    [+] UPDATING RESULTS...
    [+] DELETING TEST INDEX...
    <span style="color:red">[+] TEST ( test_4 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_1 :</span>
    [+] A NEW INDEX ( test_agg_1 ) WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    <span style="color:orange">[+] TESTING RULE -- AGG_RULE01 ( ./agg_rule01.yaml )</span>
    [+] UPDATING RESULTS...
    [+] DELETING TEST INDEX...
    <span style="color:red">[+] TEST ( test_agg_1 ) FAILED</span>

<span style="color:#779ECB">[+] RUNNING test_agg_02 :</span>
    <span style="color:orange">[+] TEST ( test_agg_2 ) WAS DISABLED</span>


<span style="color:orange">[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json</span>

    ╒════════════╤══════════╤═════════════════════════════════════════════════════════════╕
    │ TestID     │ RESULT   │ MESSAGE                                                     │
    ╞════════════╪══════════╪═════════════════════════════════════════════════════════════╡
    │ test_1     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_2     │ PASSED   │                                                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_3     │ FAILED   │ &gt; 1 LOG(S) MATCHED: log001.json                             │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_4     │ FAILED   │ &gt; 7 LOG(S) DID NOT MATCH: agg_log001.json, agg_log002.json, │
    │            │          │   agg_log003.json, agg_log004.json, agg_log005.json,        │
    │            │          │   log001.json, log003.json                                  │
    ├────────────┼──────────┼─────────────────────────────────────────────────────────────┤
    │ test_agg_1 │ FAILED   │ &gt; HITS (5) EXCEEDED THE THRESHOLD                           │
    ╘════════════╧══════════╧═════════════════════════════════════════════════════════════╛
</code></pre></div></div>
