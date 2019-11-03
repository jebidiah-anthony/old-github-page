---
layout: default
title: "elastalerter"
description: "Tests rules if they match 100% accurately."
header-img: ""
tags: [elastalert, elastalert-test-rule]
---

# ./elastalerter.py

---

## ENVIRONMENT

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

- This probably won't work on Windows Machines.
- The program manually sets the rule's alert to __`elastalerter.alerter.Alert`__.
- The program manually creates a basic config file if none is specified.

---

## SET-UP

1. Download and run [elasticsearch 7.4.0](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz) for Linux.

   ```console
   $ tar xvf elasticsearch-7.4.0-linux-x86_64.tar.gz

     ...omitted...

   $ elasticsearch-7.4.0/bin/elasticsearch

     ...omitted...

   ```

2. Set-up a python virtual environment:

   ```console
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

   ```console
<<<<<<< HEAD
   (v_env) $ wget https://github.com/jebidiah-anthony/elastalerter/blob/master/elastalerter.zip?raw=true
   ```
   ```
=======
   (v_env) $ wget https://jebidiah-anthony.github.io/prjct/files/elastalerter.zip
   
>>>>>>> d52d98a12679bee1567e6812b90f1a32b7f39680
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
   
   (v_env) $ pip install --requirement requirements.txt
   
     ...omitted...
     Installing collected packages: pytz, tzlocal, six, APScheduler, urllib3, idna, certifi, chardet, requests, 
     aws-requests-auth, blist, docutils, jmespath, python-dateutil, botocore, s3transfer, boto3, pycparser, cffi, 
     configparser, croniter, defusedxml, docopt, jsonschema, mock, PyStaticConfiguration, stomp.py, exotel, 
     envparse, python-magic, pbr, oauthlib, requests-oauthlib, requests-toolbelt, jira, PyYAML, PySocks, PyJWT, 
     twilio, texttable, elasticsearch, future, thehive4py, elastalert, tabulate
     ...omitted...
   
   (v_env) $ pip install .
   
     ...omitted...
     Successfully built elastalerter
     Installing collected packages: elastalerter
     Successfully installed elastalerter-0.0.1

   ```

---

## EXECUTION (w/ sample output)

### help (__`-h, --help`__)
```console
(v_env) $ python elastalerter.py -h
<<<<<<< HEAD
```
```
usage: ./test.py --logs LOGS_DIR --rules RULES_DIR --expected expected.json

    SAMPLE "expected.json"
    ------------------------------------------------
    {
        "test_id": {
            "rule": "rule.yaml",
            "log": ["log1.json", "log2.json", ...],
            "match": (True | False)
        },
        "test_id": {
            ...
        }
    }

optional arguments:
  -h, --help       show this help message and exit
  --host HOST      elasticsearch instance host address (default: 127.0.0.1)
  --port PORT      elasticsearch instance port (default: 9200)
  --config YAML    elastalert config file to use.
  -v, --verbose    output other details

required arguments:
  --expected JSON  JSON outline of test names and expected results
  --logs DIR       directory of the logs to be indexed
  --rules DIR      directory of the rules to run with elastalert
```

### default output
```console
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json
```
```
[+] RUNNING test_1

    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] TEST ( test_1 ) PASSED

[+] RUNNING test_2

    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] TEST ( test_2 ) PASSED

[+] RUNNING test_3

    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] TEST ( test_3 ) PASSED

[+] RUNNING test_4

    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] TEST ( test_4 ) PASSED

[+] RUNNING test_5

    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] TEST ( test_5 ) FAILED

[+] RUNNING test_6

    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] TEST ( test_6 ) FAILED

[+] RUNNING test_agg_1

    [+] TESTING RULE ( ./rules/agg_rule01.yml )
    [+] TEST ( test_agg_1 ) FAILED

[+] RUNNING test_agg_2

    [+] TESTING RULE ( ./rules/agg_rule01.yml )
    [+] TEST ( test_agg_2 ) FAILED

[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json

    ╒════════════╤══════════╤═══════════════════════════════════╕
    │ TestID     │ RESULT   │ MESSAGE                           │
    ╞════════════╪══════════╪═══════════════════════════════════╡
    │ test_1     │ PASSED   │                                   │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_2     │ PASSED   │                                   │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_3     │ PASSED   │                                   │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_4     │ PASSED   │                                   │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_5     │ FAILED   │ > MATCHED: log001.json            │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_6     │ FAILED   │ > NO LOG(S) MATCHED.              │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_agg_1 │ FAILED   │ > HITS (5) EXCEEDED THE THRESHOLD │
    ├────────────┼──────────┼───────────────────────────────────┤
    │ test_agg_2 │ FAILED   │ > NO LOG(S) MATCHED.              │
    ╘════════════╧══════════╧═══════════════════════════════════╛

```

### verbose (__`-v, --verbose`__)
```console
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json --verbose
```
```
[+] RUNNING test_1

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_1 ) PASSED

[+] RUNNING test_2

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_2 ) PASSED

[+] RUNNING test_3

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_3 ) PASSED

[+] RUNNING test_4

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_4 ) PASSED

[+] RUNNING test_5

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_5 ) FAILED

[+] RUNNING test_6

    [+] INDEXING SPECIFIED LOGS...
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
    [+] TEST ( test_6 ) FAILED

[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json

    ╒══════════╤══════════╤════════════════════════╕
    │ TestID   │ RESULT   │ MESSAGE                │
    ╞══════════╪══════════╪════════════════════════╡
    │ test_1   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_2   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_3   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_4   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_5   │ FAILED   │ > MATCHED: log001.json │
    ├──────────┼──────────┼────────────────────────┤
    │ test_6   │ FAILED   │ > NO LOG(S) MATCHED.   │
    ╘══════════╧══════════╧════════════════════════╛

```

### very verbose (__`-vv`__)
```console
(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json -vv
```
```
[+] RUNNING test_1

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log001.json WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000001" WAS DELETED
    [+] TEST ( test_1 ) PASSED

[+] RUNNING test_2

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log002.json WAS UPDATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000002" WAS DELETED
    [+] TEST ( test_2 ) PASSED

[+] RUNNING test_3

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log002.json WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000002" WAS DELETED
    [+] TEST ( test_3 ) PASSED

[+] RUNNING test_4

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log001.json WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000001" WAS DELETED
    [+] TEST ( test_4 ) PASSED

[+] RUNNING test_5

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log001.json WAS CREATED
        [+] ./logs/log003.json WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule01.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000001" WAS DELETED
        [+] "log-00000003" WAS DELETED
    [+] TEST ( test_5 ) FAILED

[+] RUNNING test_6

    [+] INDEXING SPECIFIED LOGS...
        [+] ./logs/log001.json WAS CREATED
        [+] ./logs/log003.json WAS CREATED
    [+] TIMESTAMP RANGE -- [2019-09-16T15:59:57 - 2019-09-16T15:59:57]
    [+] TESTING RULE ( ./rules/rule02.yml )
    [+] UPDATING RESULTS...
    [+] CLEARING INDEXED LOGS...
        [+] "log-00000001" WAS DELETED
        [+] "log-00000003" WAS DELETED
    [+] TEST ( test_6 ) FAILED

[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json

    ╒══════════╤══════════╤════════════════════════╕
    │ TestID   │ RESULT   │ MESSAGE                │
    ╞══════════╪══════════╪════════════════════════╡
    │ test_1   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_2   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_3   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_4   │ PASSED   │                        │
    ├──────────┼──────────┼────────────────────────┤
    │ test_5   │ FAILED   │ > MATCHED: log001.json │
    ├──────────┼──────────┼────────────────────────┤
    │ test_6   │ FAILED   │ > NO LOG(S) MATCHED.   │
    ╘══════════╧══════════╧════════════════════════╛
=======

    usage: ./test.py --logs LOGS_DIR --rules RULES_DIR --expected expected.json

      SAMPLE "expected.json"
      ------------------------------------------------
      {
          "test_id": {
              "rule": "rule.yaml",
              "log": ["log1.json", "log2.json", ...],
              "match": (True | False)
          },
          "test_id": {
              ...
          }
      }

  optional arguments:
    -h, --help          show this help message and exit
    --host HOST         elasticsearch instance host address (default: 127.0.0.1)
    --port PORT         elasticsearch instance port (default: 9200)
    --config YAML       elastalert config file to use.
    -r RULE [RULE ...]  filename(s) of specific rule(s) to be tested

  required arguments:
    --expected JSON     JSON outline of test names and expected results
    --logs DIR          directory of the logs to be indexed
    --rules DIR         directory of the rules to run with elastalert

(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json

  [+] INDEXING LOGS FROM "./logs" ... 

  	[ERROR] "test.json" IS NOT A VALID LOG FILE
  	[ERROR] "test.yaml" IS NOT A VALID JSON FILE
  
  [+] TIMESTAMP RANGE: (2019-09-16T15:59:57.000Z) - (2019-09-16T15:59:57.000Z)
  
  [+] RUNNING ELASTALERT-TEST-RULE...
  
  	[+] TESTING RULE (./rules/rule01.yaml)
  	[+] TESTING RULE (./rules/rule02.yaml)
  	[ERROR] (test_file) FILE EXTENTSION DOESN'T SEEM TO BE ".yaml" OR ".yml"
  
  [+] GENERATING REPORT...
  
  	[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json
  
  	╒═════════╤══════════╤═════════════════════════════════════════╕
  	│ TestID  │ RESULT   │ MESSAGE                                 │
  	╞═════════╪══════════╪═════════════════════════════════════════╡
  	│ test_1  │ PASSED   │ N/A                                     │
  	├─────────┼──────────┼─────────────────────────────────────────┤
  	│ test_2  │ PASSED   │ N/A                                     │
  	├─────────┼──────────┼─────────────────────────────────────────┤
  	│ test_3  │ PASSED   │ N/A                                     │
  	├─────────┼──────────┼─────────────────────────────────────────┤
  	│ test_4  │ PASSED   │ N/A                                     │
  	├─────────┼──────────┼─────────────────────────────────────────┤
  	│ test_5  │ FAILED   │ MATCHED: log001.json                    │
  	├─────────┼──────────┼─────────────────────────────────────────┤
  	│ test_6  │ FAILED   │ DID NOT MATCH: log001.json, log003.json │
  	╘═════════╧══════════╧═════════════════════════════════════════╛
  
  [+] DELETING INDEXED LOGS...

  [+] DONE

(v_env) $ python elastalerter.py --logs ./logs --rules ./rules --expected ./expected.json -r rule01.yaml

  [+] INDEXING LOGS FROM "./logs" ... 
  
  	[ERROR] "test.json" IS NOT A VALID LOG FILE
  	[ERROR] "test.yaml" IS NOT A VALID JSON FILE
  
  [+] TIMESTAMP RANGE: (2019-09-16T15:59:57.000Z) - (2019-09-16T15:59:57.000Z)
  
  [+] RUNNING ELASTALERT-TEST-RULE...
  
  	[+] TESTING RULE (./rules/rule01.yaml)
  
  [+] GENERATING REPORT...
  
  	[+] RESULTS WERE OUTPUT TO CURRENT_WORKING_DIRECTORY/results.json
  
  	╒══════════╤══════════╤════════════════════════════════════════╕
  	│ TestID   │ RESULT   │ MESSAGE                                │
  	╞══════════╪══════════╪════════════════════════════════════════╡
  	│ test_1   │ PASSED   │ N/A                                    │
  	├──────────┼──────────┼────────────────────────────────────────┤
  	│ test_2   │ N/A      │ 'rule02.yaml' WAS NOT TESTED/SPECIFIED │
  	├──────────┼──────────┼────────────────────────────────────────┤
  	│ test_3   │ PASSED   │ N/A                                    │
  	├──────────┼──────────┼────────────────────────────────────────┤
  	│ test_4   │ N/A      │ 'rule02.yaml' WAS NOT TESTED/SPECIFIED │
  	├──────────┼──────────┼────────────────────────────────────────┤
  	│ test_5   │ FAILED   │ MATCHED: log001.json                   │
  	├──────────┼──────────┼────────────────────────────────────────┤
  	│ test_6   │ N/A      │ 'rule02.yaml' WAS NOT TESTED/SPECIFIED │
  	╘══════════╧══════════╧════════════════════════════════════════╛
  
  [+] DELETING INDEXED LOGS...
  
  [+] DONE
>>>>>>> d52d98a12679bee1567e6812b90f1a32b7f39680

```

