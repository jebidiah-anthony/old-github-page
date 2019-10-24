from elastalert.alerts import Alerter, BasicMatchString
import json

class Alert(Alerter):

    required_options = set(['name'])

    def alert(self, matches):

        for match in matches:

            with open("/tmp/alert_test_results.log", "a") as output_file:
                
                alert_data = {
                    'rule': self.rule["name"],
                    'index': match['_index'],
                    'id': match['_id']
                }

                json.dump(alert_data, output_file)
                output_file.write("\n")

    def get_info(self):
        info = {
            'type': 'elastalert test alerter',
            'name': self.rule['name'],
            'output_file': '/tmp/alert_test_results.log'
        }
        
        return info
