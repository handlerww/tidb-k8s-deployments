#!/usr/bin/env python
# coding=utf-8
from kubernetes import client, config, utils
from requests.packages import urllib3
import json
import yaml
from flask import Flask
from flask import request
from flask import make_response
from flask_cors import *

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

base_path = ''
urllib3.disable_warnings()


app = Flask(__name__)
CORS(app)


def get_k8s_handler(APISERVER, Token):
    configuration = client.Configuration()
    configuration.host = APISERVER
    #     for developement server
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + Token}
    client.Configuration.set_default(configuration)
    return client


def create_deployment(k8s_client, namespace,
                      pd_replicates, tikv_replicates,tidb_replicates,
                       pd_version,tikv_version,tidb_version):
    utils.create_from_yaml(k8s_client.ApiClient(),
                            "./yaml/configmap.yaml", namespace=namespace)
    utils.create_from_yaml(k8s_client.ApiClient(),
                            "./yaml/service.yaml", namespace=namespace)
    with open("./yaml/simple-pd-stateful.yaml") as f:
        dep = yaml.safe_load(f)
        dep['spec']['replicas'] = pd_replicates
        dep['spec']['template']['spec']['containers'][0]['image'] = "pingcap/pd:v"+pd_version
        k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)
    with open("./yaml/simple-tikv-stateful.yaml") as f:
        dep = yaml.safe_load(f)
        dep['spec']['replicas'] = tikv_replicates
        dep['spec']['template']['spec']['containers'][0]['image'] = "pingcap/tikv:v"+tikv_version
        k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)
    with open("./yaml/simple-tidb-stateful.yaml") as f:
        dep = yaml.safe_load(f)
        dep['spec']['replicas'] = tidb_replicates
        dep['spec']['template']['spec']['containers'][1]['image'] = "pingcap/tidb:v"+tidb_version
        k8s_client.AppsV1Api().create_namespaced_stateful_set(body=dep, namespace=namespace)
    with open("./yaml/simple-monitor-deployment.yaml") as f:
        dep = yaml.safe_load(f)
        for item in dep['items']:
            if item['kind'] == 'ClusterRoleBinding':
                item['subjects'][0]['namespace'] = namespace
        try:
            k8s_client.RbacAuthorizationV1beta1Api().delete_cluster_role(name='basic-monitor')
        except:
            pass
        try:
            k8s_client.RbacAuthorizationV1beta1Api().delete_cluster_role_binding(name='basic-monitor')
        except:
            pass
        utils.create_from_dict(
            k8s_client.ApiClient(), data=dep, namespace=namespace)
    return('ok')
    


def create_namespaces(k8s_client, namespace):
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


def release_namespaces(k8s_client, namespace):
    k8s_client.CoreV1Api().delete_namespace(name=namespace, body={})
    return('ok')


def get_status(k8s_client):
    ret = k8s_client.CoreV1Api().list_namespace(
        label_selector='application=tidb', watch=False)
    result = {}
    for namespace in ret.items:
        for sts in (k8s_client.AppsV1Api().list_namespaced_stateful_set(namespace=namespace.metadata.name)).items:
            result[sts.metadata.labels['app.kubernetes.io/component']] = {
                'ready': str(sts.status.ready_replicas), 'replicas': str(sts.status.replicas),
                'namespace':str(namespace.metadata.name)}
    if result != {}:
        return(result)
    else:
        return()


@app.route('/deploy', methods=['POST'])
def web_deploy():
    try:
        request_params = request.get_json()
        # precheck
        if request_params['pd_replicates']<0 or request_params['tikv_replicates']<0 or request_params['tidb_replicates']<0:
            raise Exception("Replicates Number Error")
        if type(request_params['pd_replicates'])!=int or type(request_params['tikv_replicates'])!=int or type(request_params['tidb_replicates'])!=int:
            raise Exception("KeyError")
        if request_params['pd_version']=='' or request_params['tikv_version']=='' or request_params['tidb_version']=='':
            raise Exception("KeyError")    
        k8s_client = get_k8s_handler(
            APISERVER=request_params['apiserver'], Token=request_params['api_token'])
        server = {
            'apiserver': request_params['apiserver'], 'token': request_params['api_token']}
        request_params.pop('apiserver')
        request_params.pop('api_token')
    
        create_namespaces(k8s_client, namespace=request_params['namespace'])
        create_deployment(k8s_client, **request_params)
        for i in serverlist:
            if i['apiserver'] == server['apiserver']:
                serverlist.remove(server)
        serverlist.append(server)
        with open('serverlist.json', 'w') as fp:
            json.dump(serverlist, fp=fp)
        resp = make_response('ok', 200)
        return resp
    except KeyError:
        resp = make_response('KeyError', 500)
        return resp
    except Exception as e:
        if 'exists' in str(e):
            resp = make_response('Resources exists, check your configuration.', 500)
            return resp
        elif 'NoneType' in str(e):
            resp = make_response('Paramaters Error.', 500)
            return resp
        elif 'Unauthorized' in str(e):
            resp = make_response('Unauthorized.', 500)
            return resp
        elif 'not supported between instances' in str(e):
            resp = make_response('Paramaters Type Error.', 500)
            return resp
        else:
            resp = make_response(str(e), 500)
            return resp

@app.route('/status', methods=['GET'])
def web_status():
    result = []
    for server in serverlist:
        k8s_client = get_k8s_handler(
            APISERVER=server['apiserver'], Token=server['token'])
        status = get_status(k8s_client)
        if(status):
            result.append({'namespace':status['pd']['namespace'],'node':server['apiserver'],'status':'pd:'+status['pd']['ready']+'/'+status['pd']['replicas']+' tikv:'+status['tikv']['ready']+'/'+status['tikv']['replicas']+' tidb:'+status['tidb']['ready']+'/'+status['tidb']['replicas']})
        else:
            serverlist.remove(server)
    resp = make_response(json.dumps(result), 200)
    return resp


@app.route('/delete', methods=['POST'])
def web_delete():
    try:
        request_params = request.get_json()
        server ={}
        for i in serverlist:
            if request_params['apiserver'] in i['apiserver']:
                server=i
        if server == {}:
            raise Exception("Cluster Not Found")
        k8s_client = get_k8s_handler(
            APISERVER=server['apiserver'], Token=server['token'])
        result = release_namespaces(k8s_client, namespace=request_params['namespace'])
        if result == 'ok':
            for i in serverlist:
                if request_params['apiserver'] in i['apiserver']:
                    serverlist.remove(i)
            with open('serverlist.json', 'w') as fp:
                json.dumps(serverlist, file=fp)
        resp = make_response('ok', 200)
        return resp
    except KeyError as e:
        resp = make_response('Cluster Not Found', 200)
        return resp
    except Exception as e:
        if 'Not Found' in str(e):
            resp = make_response('Cluster Not Found', 200)
            return resp
        else:
            resp = make_response(str(e), 200)
            return resp
    # k8s handler non exists 连接不上
    # namespace non exists 命名空间不存在
    # serverlist read error serverlist没有更新


if __name__ == '__main__':
    serverlist = []
    try:
        with open('serverlist.json', 'r') as fp:
            serverlist = json.load(fp=fp)
    except:
        serverlist = []
    app.run()
