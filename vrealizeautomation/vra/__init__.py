import requests
import json
from requests.packages import urllib3
import pandas as pd
from datetime import datetime

class vraauthentication:
    # Authenticates to VRA
    # Post authentication, obtains the bearer token. 
    def __init__(self, 
                 vra_base_fqdn, 
                 vra_tenant_name,
                 vra_id,
                 vra_password):

        self.vra_base_fqdn = vra_base_fqdn
        self.vra_tenant_name = vra_tenant_name
        self.vra_id = vra_id
        self.vra_password = vra_password
    pass
    
    def get_vra_bearer_token(self):
        # Post request url to obtain the bearer token.
        vra_bearer_token_request_url = self.vra_base_fqdn + '/identity/api/tokens'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        vra_authentication_payload = json.dumps({
            "username": self.vra_id,
            "password": self.vra_password,
            "tenant": self.vra_tenant_name})
        vra_authentication_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        try:
            bearer_token_request = requests.post(
                    vra_bearer_token_request_url, 
                    headers=vra_authentication_headers, 
                    data=vra_authentication_payload, 
                    verify=False)
            bearer_token_request_response = json.loads(
                    bearer_token_request.content.decode('utf-8'))

            bearer_token_validity = bearer_token_request_response["expires"]
            bearer_token_id = bearer_token_request_response["id"]
            self.vra_bearer_token = bearer_token_id
            self.vra_bearer_authentication_header = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + self.vra_bearer_token
            }
            if bearer_token_request.status_code == 200:
                print("VRA Authentication Successful and will be valid until : " +
                    bearer_token_validity)
                return True
        except Exception as error:
            print("Failed to obtain a bearer token from vRealize Automation.")
            print(error)
            return False
    
    def obtain_deployments_info(self):
        self.all_deployments_df = pd.DataFrame(columns=['Deployment_Name', 'Submitted_Date', 'Requested_By', 'Requested_For','Deployment ID', 'Deployment State'])
        get_all_deployments_url = self.vra_base_fqdn + '/catalog-service/api/consumer/deployments'
        get_all_deployments = requests.get(
            get_all_deployments_url, headers=self.vra_bearer_authentication_header, verify=False)
        get_all_deployments_response_content = json.loads(
            get_all_deployments.content.decode('utf-8'))
        deployments_count = get_all_deployments_response_content['metadata']['totalElements']
        number_of_pages = deployments_count // 100 + 1  
        print('Total Number of Deployments : ', deployments_count)
        print('Total Number of Deployments spanned across pages : ', number_of_pages)

        for page in range(number_of_pages):
            page_number = page + 1
            params_payload = {
                'page': page_number,
                'limit': 100
            }
            requested_page_info = requests.get(
                get_all_deployments_url, params=params_payload,
                headers=self.vra_bearer_authentication_header, 
                verify=False)
            deployments_in_page = json.loads(
                requested_page_info.content.decode('utf-8'))

            for each_deployment in deployments_in_page['content']:
                # print(each_deployment)
                if each_deployment['request'] is not None:
                    each_line = {'Deployment_Name': each_deployment['name'],
                                 'Requested_By' : each_deployment['request']['requestedBy'],
                                 'Requested_For' : each_deployment['request']['requestedFor'],
                                 'Submitted_Date': each_deployment['request']['dateSubmitted'],
                                 'Deployment ID':  each_deployment['request']['id'],
                                 'Deployment State': each_deployment['request']['phase'],
                                #  'Deployment Status': each_deployment['request']['completionDetailMessage']
                             }
                    self.all_deployments_df = self.all_deployments_df.append(each_line,ignore_index=True)
                    # print(each_line)
        # print(self.all_deployments_df)

        time_now = datetime.now()
        report_time = time_now.strftime("%d-%b-%Y-%H-%M-%S")
        report_file_name = 'vRealize-DeploymentsReport-' + report_time + '.xlsx'
        self.all_deployments_df.to_excel(report_file_name, index=False)
        print("Deployment reported saved as : " + report_file_name)


