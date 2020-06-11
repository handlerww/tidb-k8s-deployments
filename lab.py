# Experiments for Kubernetes Python Client Features

from kubernetes import client, config,utils
import yaml
import json
from requests.packages import urllib3
urllib3.disable_warnings()

def get_k8s_handler(APISERVER,Token):
    configuration = client.Configuration()
    configuration.host = APISERVER
    #     for developement server
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + Token}
    client.Configuration.set_default(configuration)
    return client


def create_deployment(k8s_client,namespace): 
    try:
        utils.create_from_yaml(k8s_client.ApiClient(), "./yaml/configmap.yaml",namespace=namespace)
        utils.create_from_yaml(k8s_client.ApiClient(), "./yaml/service.yaml",namespace=namespace)
        with open("./yaml/simple-pd-stateful.yaml") as f:
            dep = yaml.safe_load(f)
            dep['spec']['replicas']=3
            dep['spec']['template']['spec']['containers'][0]['image']="pingcap/pd:v3.0.13"
            k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)
        with open("./yaml/simple-tikv-stateful.yaml") as f:
            dep = yaml.safe_load(f)
            dep['spec']['replicas']=3
            dep['spec']['template']['spec']['containers'][0]['image']="pingcap/tikv:v3.0.13"
            k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)
        with open("./yaml/simple-tidb-stateful.yaml") as f:
            dep = yaml.safe_load(f)
            dep['spec']['replicas']=3
            dep['spec']['template']['spec']['containers'][1]['image']="pingcap/tidb:v3.0.13"
            k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)      
        with open("./yaml/simple-monitor-deployment.yaml") as f:
            dep = yaml.safe_load(f)
            for item in dep['items']:
                if item['kind'] =='ClusterRoleBinding':
                    item['subjects'][0]['namespace']=namespace
            utils.create_from_dict(k8s_client.ApiClient(),data=dep, namespace=namespace)
        return('ok')
    except Exception as e:
        print(e)
        if 'Error from server (Conflict): ' in str(e):
            return('Resources is existed, check your configuration.')
        
def create_namespaces(k8s_client,namespace):
    try:
        k8s_client.CoreV1Api().create_namespace(body={
          "metadata": {
              "name": namespace,
              "labels":
                {
                    "application": "tidb",
                }
              }
          })
        return ('ok')
    except Exception as e:
        exception_type = json.loads(e.body)['reason']
        if exception_type == "AlreadyExists":
            return('Namespace is existed, check your configuration.')
    
def release_namespaces(k8s_client,namespaces):
    k8s_client.CoreV1Api().delete_namespace(name=namespaces, body={})
    
def get_status(k8s_client):
    ret = k8s_client.CoreV1Api().list_namespace(label_selector='application=tidb',watch=False)
    result ={}
    for namespace in ret.items:
        for sts in (k8s_client.AppsV1Api().list_namespaced_stateful_set(namespace=namespace.metadata.name)).items:
            result[sts.metadata.labels['app.kubernetes.io/component'] ]={'ready':str(sts.status.ready_replicas),'replicas':str(sts.status.replicas)}
    print(result)
if __name__ == '__main__':
    # Temporary k8s Clutser for developing
    k8s_client = get_k8s_handler(APISERVER = 'https://47.113.195.245:6443',Token='eyJhbGciOiJSUzI1NiIsImtpZCI6IkZack1lcjY5SzRkc0UxaTUtZE00S0lqNWpEZnRDVUpjMEFZZ0M2TEZ2TUkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLW1neG1qIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJmNmYwN2NlZS0xOTJmLTQ3YmMtOWRhNi1lZmQxMDQzYWY1YzkiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.Xo4RpuG2LuOCchgsAKxMGHIljDt5zl-fpxcZiFnCexVmnF4vtEjXqGXVb-BoZf9UbYbhmiQlh9iuL1ImURUYrPFoZXGyxsOZZmlXkJZIsiB8JAsc2vtM5CB7ESsG1-T6DltxngtwTIlsJ9Zqvo9YF288Hj1oVUsz9Oq0lCT8DFR_4NJ3lK-K8s7Iv12amz87Y2PnlGpVRoW3d9Xxy0SS76B3S5x3PMUZau_FhzqqE-LJXnHjUSBm39zeZ6EXeIbd17EaO_j9mN40UoYhV7LOKwj_2xql7ojsAVXJBdy77FPWQAPjvR5hGmQc83VmORZcX7-MxNrUGJwrLIkr7940oA')
    
    print(create_namespaces(k8s_client,'try'))
    print(create_deployment(k8s_client,'try'))
    get_status(k8s_client)
    release_namespaces(k8s_client,'try')