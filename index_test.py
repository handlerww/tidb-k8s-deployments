import requests
import unittest
import json
# Task1 get function work right

class index_test(unittest.TestCase):
    api_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZack1lcjY5SzRkc0UxaTUtZE00S0lqNWpEZnRDVUpjMEFZZ0M2TEZ2TUkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLW1neG1qIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJmNmYwN2NlZS0xOTJmLTQ3YmMtOWRhNi1lZmQxMDQzYWY1YzkiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.Xo4RpuG2LuOCchgsAKxMGHIljDt5zl-fpxcZiFnCexVmnF4vtEjXqGXVb-BoZf9UbYbhmiQlh9iuL1ImURUYrPFoZXGyxsOZZmlXkJZIsiB8JAsc2vtM5CB7ESsG1-T6DltxngtwTIlsJ9Zqvo9YF288Hj1oVUsz9Oq0lCT8DFR_4NJ3lK-K8s7Iv12amz87Y2PnlGpVRoW3d9Xxy0SS76B3S5x3PMUZau_FhzqqE-LJXnHjUSBm39zeZ6EXeIbd17EaO_j9mN40UoYhV7LOKwj_2xql7ojsAVXJBdy77FPWQAPjvR5hGmQc83VmORZcX7-MxNrUGJwrLIkr7940oA"

    # Deployment
    def test0(self):
        self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps({'api_token': api_token,
                                                                                         'apiserver': "https://47.113.195.245:6443",
                                                                                         'namespace': "try",
                                                                                         'pd_replicates': 1,
                                                                                         'pd_version': "3.0.13",
                                                                                         'tidb_replicates': 1,
                                                                                         'tidb_version': "3.0.13",
                                                                                         'tikv_replicates': 1,
                                                                                         'tikv_version': "3.0.13"}), headers={"Content-Type": "application/json"}).text, 'ok', 'Cluster Deployments Fails')

    def test1(self):
        self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps({'api_token': api_token,
                                                                                         'apiserver': "https://47.113.195.245:6443",
                                                                                         'namespace': "try",
                                                                                         'pd_replicates': 0,
                                                                                         'pd_version': "3.0.13",
                                                                                         'tidb_replicates': 0,
                                                                                         'tidb_version': "3.0.13",
                                                                                         'tikv_replicates': 0,
                                                                                         'tikv_version': "3.0.13"}), headers={"Content-Type": "application/json"}).text, 'Resources exists, check your configuration.', 'Resouces Existence Check Fails')

    def test2(self):
        self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps({'api_token': api_token,
                                                                                        'apiserver': "https://47.113.195.245:6443",
                                                                                        'namespace': "try",
                                                                                        'pd_replicates': -3,
                                                                                        'pd_version': "3.0.13",
                                                                                        'tidb_replicates': -2,
                                                                                        'tidb_version': "3.0.13",
                                                                                        'tikv_replicates': -3,
                                                                                        'tikv_version': "3.0.13"}), headers={"Content-Type": "application/json"}).text, "Replicates Number Error", msg="Negetive Number Test Fails")

    def test3(self):
        self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps({'api_token': 'error',
                                                                                    'apiserver': "https://47.113.195.245:6443",
                                                                                    'namespace': "try",
                                                                                    'pd_replicates': 3,
                                                                                    'pd_version': "3.0.13",
                                                                                    'tidb_replicates': 2,
                                                                                    'tidb_version': "3.0.13",
                                                                                    'tikv_replicates': 3,
                                                                                    'tikv_version': "3.0.13"}), headers={"Content-Type": "application/json"}).text, "Unauthorized.", msg="Authorized Test Fails")
    def test_paramaters_absent(self):
        para = {'api_token': api_token,
        'apiserver': "https://47.113.195.245:6443",
        'namespace': "try",
        'pd_replicates': 1,
        'pd_version': "3.0.13",
        'tidb_replicates': 1,
        'tidb_version': "3.0.13",
        'tikv_replicates': 1,
        'tikv_version': "3.0.13"}
        for i in para.items():
            para_for_test = para.copy()
            para_for_test.pop(i[0])
            self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps(para_for_test), headers={"Content-Type": "application/json"}).text, "KeyError", msg="KeyError Test Fails")
    def test_paramaters_type_error(self):
        para = {'api_token': api_token,
        'apiserver': "https://47.113.195.245:6443",
        'namespace': "try",
        'pd_replicates': 'a',
        'pd_version': "3.0.13",
        'tidb_replicates': 1,
        'tidb_version': "3.0.13",
        'tikv_replicates': 1,
        'tikv_version': "3.0.13"}
        self.assertEqual(requests.post("http://127.0.0.1:5000/deploy", data=json.dumps(para), headers={"Content-Type": "application/json"}).text, "Paramaters Type Error.", msg="Paramaters Type Test Fails")

    # Status:
    # def test_status(self):
    #     self.assertEqual(requests.get('http://127.0.0.1:5000/status').text,'[{"pd": {"ready": "1", "replicas": "1"}, "tidb": {"ready": "1", "replicas": "1"}, "tikv": {"ready": "1", "replicas": "1"}}]',msg='Status Function Fails')
    # Deletes:
    def test_delete(self):
         self.assertEqual(requests.post('http://127.0.0.1:5000/delete',data=json.dumps({'apiserver':'https://47.113.195.245:6443','namespace':'try'}), headers={"Content-Type": "application/json"}).text,'ok',msg='Delete Function Fails')
    def test_delete_ns_err(self):
         self.assertEqual(requests.post('http://127.0.0.1:5000/delete',data=json.dumps({'apiserver':'https://47.113.195.245:6443','namespace':'error'}), headers={"Content-Type": "application/json"}).text,'Cluster Not Found',msg='Delete Function Fails')

if __name__ == '__main__':
    unittest.main()
