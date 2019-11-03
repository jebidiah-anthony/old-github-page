from datetime import timedelta as dtd
from elasticsearch import Elasticsearch
from tabulate import tabulate
import argparse
import dateutil.parser as dp
import json
import os
import time

parser = argparse.ArgumentParser(
    prog='./test.py',
    usage="%(prog)s --logs LOGS_DIR --rules RULES_DIR --expected expected.json",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
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
    }'''
)

parser.add_argument('--host', default="127.0.0.1", type=str, help='elasticsearch instance host address (default: %(default)s)')
parser.add_argument('--port', default=9200, type=int, help='elasticsearch instance port (default: %(default)d)')
parser.add_argument('--config', metavar="YAML", type=str, help='elastalert config file to use.')
parser.add_argument('-r', default=[], metavar="RULE", nargs="+", help='filename(s) of specific rule(s) to be tested')

arg_group = parser.add_argument_group('required arguments')
arg_group.add_argument('--expected', metavar="JSON", required=True, type=str, help='JSON outline of test names and expected results')
arg_group.add_argument('--logs', metavar="DIR", required=True, type=str, help='directory of the logs to be indexed')
arg_group.add_argument('--rules', metavar="DIR", required=True, type=str, help='directory of the rules to run with elastalert')

args = parser.parse_args()

es = Elasticsearch([{'host':args.host, 'port':args.port}])
if not es.ping():
    print("\n\t[ERROR] CONNECTING TO ELASTICSEARCH FAILED\n")
    exit()

test_results = {
    "total": 0,
    "pass": 0,
    "fail": 0,
    "tests": dict()
}

log_refs = dict()
timestamp_strt = str()
timestamp_last = str()

def checkFileExistence(arg_file):
    if not os.path.exists(arg_file):
        print(f"\n\t[ERROR] THE FILE \"{arg_file}\" DOES NOT EXIST\n")
        return False
    return True

def indexLogs(log_dir):
    global log_refs
    log_files = sorted(os.listdir(log_dir))
    
    for log_file in log_files:
        with open(log_dir + "/" + log_file) as log:
            try:
                log_json = json.load(log)
                index = log_json['_index']
                id = log_json['_id']
                
                try:
                    res = es.index(index=index, id=id, doc_type=log_json['_type'], body=log_json['_source'])
                    file_ref = {log_file: list()}
                    log_refs.setdefault(index + "/\\" + id, file_ref)

                    timestamp = log_json['_source']['real_timestamp']
                    updateLogRange(timestamp)
                    
                except:
                    print("\t[ERROR]" + log_dir + "/" + log_file + " WAS NOT INDEXED")
                    
            except KeyError:
                print("\t[ERROR] \"{}\" IS NOT A VALID LOG FILE".format(log_file))
        
            except json.decoder.JSONDecodeError:
                print("\t[ERROR] \"{}\" IS NOT A VALID JSON FILE".format(log_file))

def deleteLogs(log_refs):
    for i in log_refs:
        curr = i.split("/\\")
        try: res = es.delete(index=curr[0], id=curr[1])
        except: print("\t" + curr[0] + "-" + curr[1] + " | was not deleted")
            
def updateLogRange(timestamp):    
    global timestamp_strt
    global timestamp_last
    
    if timestamp_strt == "" and timestamp_last == "":
        timestamp_strt = timestamp
        timestamp_last = timestamp
        return
    
    if dp.parse(timestamp) > dp.parse(timestamp_last):
        timestamp_last = timestamp
    elif dp.parse(timestamp) < dp.parse(timestamp_strt):
        timestamp_strt = timestamp

def testRules(rule_dir):
    global timestamp_strt
    global timestamp_last
    
    timestamp_strt = (dp.parse(timestamp_strt[:-5]) - dtd(days=0.25)).isoformat()
    timestamp_last = (dp.parse(timestamp_last[:-5]) + dtd(days=0.25)).isoformat()
    
    if args.config == None:
        with open("/tmp/config.yaml", "w") as config_file:
            config_file.write(f"rules_folder: {args.rules}\n")
            config_file.write("\nrun_every:\n    seconds: 30\n")
            config_file.write("\nbuffer_time:\n    minutes: 5\n")
            config_file.write(f"\nes_host: {args.host}\n\nes_port: {args.port}\n")
            config_file.write("\nwriteback_index: elastalert_status\nwriteback_alias: elastalert_alerts\n ")            
            config_file.write("\nalert_time_limit:\n    minutes: 1\n")
        config = "/tmp/config.yaml"
    else: config = args.config
    
    if args.r == []: args.r = sorted(os.listdir(rule_dir))
    
    for rule_file in args.r:
        rule = rule_dir + "/" + rule_file
        
        if checkFileExistence(rule):
            if rule[-4:]==".yml" or rule[-5:]==".yaml":
                print("\t[+] TESTING RULE ({})".format(rule))
                time.sleep(0.25)
                os.system(f"elastalert-test-rule --alert --config {config} --start {timestamp_strt} --end {timestamp_last} {rule} >/dev/null 2>&1")
            else: print(f"\t[ERROR] ({rule_file}) FILE EXTENTSION DOESN'T SEEM TO BE \".yaml\" OR \".yml\"")

def tabulateResults():
    global test_results
    
    transformed_results = list()
    for i, test in enumerate(test_results['tests']):
        test_details = list()
        test_details.append(test)
        test_details.append(test_results['tests'][test].get('result', "N/A"))
        test_details.append(test_results['tests'][test].get('message', "N/A"))

        message_text = ""
        line_length = 69
        while True:
            if len(test_details[2]) < line_length:
                message_text += test_details[2]
                break
            marker = test_details[2][:line_length].rfind(" ")
            message_text += test_details[2][:marker] + "\n"
            test_details[2] = test_details[2][marker + 1:]

        if test_details[2] != "N/A": test_details[2] = message_text

        transformed_results.append(test_details)

    table = tabulate(transformed_results, headers=["TestID", "RESULT", "MESSAGE"], tablefmt="fancy_grid")
    print("\n".join("\t" + x for x in table.splitlines()))
        
def generateReport(expected_results):
    global log_refs
    global test_results
    
    alert_file = "/tmp/alert_test_results.log"
    if not os.path.exists(alert_file): open(alert_file, 'w').close()
    with open(alert_file) as results_file:
        for result in results_file:
            alert_json = json.loads(result)
            log_key = alert_json['index'] + "/\\" + alert_json['id']
            log_file = list(log_refs[log_key])[0]
            log_refs[log_key][log_file].append(alert_json['rule'])
    os.system("rm /tmp/alert_test_results.log")
            
    log_file = dict()
    for i, index_id in enumerate(log_refs):
        log_file.update(log_refs[index_id])
    log_refs = list(log_refs)
            
    with open(expected_results) as expectations_file:
        expectations = json.load(expectations_file)
    
    for i, test in enumerate(expectations):
        test_dict = dict()
        test_dict.setdefault(test, dict())
        
        rule = expectations[test]['rule'].split('.')[0]
        
        if (rule+".yml" in args.r) or (rule+".yaml" in args.r):
            rule = rule.upper()
            success = 0
            messages = list()
            for x in expectations[test]['log']:
                if expectations[test]['match'] == True:
                    if rule in log_file[x]: success += 1
                    else: messages.append(x)
                elif expectations[test]['match'] == False:
                    if rule not in log_file[x]: success += 1
                    else: messages.append(x)
            
            if success == len(expectations[test]['log']):
                test_results['pass'] += 1
                test_dict[test].setdefault("result", "PASSED")
            else:
                test_results['fail'] += 1
                test_dict[test].setdefault("result", "FAILED")
        
            if messages: 
                if expectations[test]['match']: test_dict[test].setdefault("message", "DID NOT MATCH: " + ", ".join(messages))
                else: test_dict[test].setdefault("message", "MATCHED: " + ", ".join(messages))
        else: test_dict[test].setdefault("message", f"'{expectations[test]['rule']}' WAS NOT TESTED/SPECIFIED")
            
        test_results['tests'].update(test_dict)
            
    test_results['total'] = i + 1

    results_json = json.dumps(test_results, indent=4)

    output_file = os.getcwd() + "/results.json"
    with open(output_file, 'w') as out_file:
        try: 
            out_file.write(results_json)
            print(f"\t[+] RESULTS WERE OUTPUT TO {output_file}\n")
            tabulateResults()
        except: pass

def main():
    if not checkFileExistence(args.expected): exit()
    if args.config != None:
        if not checkFileExistence(args.config): exit()
    
    log_dir = args.logs
    print("\n[+] INDEXING LOGS FROM \"{}\" ... \n".format(log_dir))
    indexLogs(log_dir)
    
    print("\n[+] TIMESTAMP RANGE: ({}) - ({})".format(timestamp_strt, timestamp_last))
    
    rule_dir = args.rules
    print("\n[+] RUNNING ELASTALERT-TEST-RULE...\n")
    testRules(rule_dir)
    
    expected_results = args.expected
    print("\n[+] GENERATING REPORT...\n")
    generateReport(expected_results)
    
    print("\n[+] DELETING INDEXED LOGS...")
    deleteLogs(log_refs)
    
    print("\n[+] DONE\n")
    
if __name__ == '__main__': main()
