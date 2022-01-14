from kubernetes import client, config
from utils import BasicConfig, cacheImage
from datetime import timezone, timedelta
import time, os

def readCache(imageName):
    listCache = []
    with open(imageName, 'r') as f:
        lines = f.read().splitlines()
        # for l in lines: listCache.append(l.split(','))
        for l in lines: listCache.append(l)
    return listCache


def getContext(imageName):
    parser = BasicConfig().parser
    tag = imageName.split(':')[-1]
    if tag.startswith('m'): return parser.get('K8S', 'PROD_CONTEXT_NAME')
    if tag.startswith('t'): return parser.get('K8S', 'STAGING_CONTEXT_NAME')


def isDeployed(imageName, kubeconfig):
    context = getContext(imageName)
    config.load_kube_config(config_file=kubeconfig, context=context)
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    # startedTime = p.status.container_statuses[0].state.running
    for p in ret.items:
        if imageName in p.spec.containers[0].image: return(True, p)
    return(False, None)


def verifySuccess(imageName, pod, kubeconfig):
    context = getContext(imageName)
    config.load_kube_config(config_file=kubeconfig, context=context)
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    startedTime = pod.status.container_statuses[0].state.running.started_at.replace(tzinfo=timezone(timedelta(hours=-7))).astimezone(timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    check = 0
    while check < 3:
        if pod.status.container_statuses[0].state.running != None: return(True, startedTime)
        time.sleep(3)
        check += 1
    if check == 3: return False


def removeCachedImage(binPath, cachedImage, listCache):
    newList = listCache
    newList.remove(cachedImage)
    if len(newList) == 0: os.remove(binPath+'/.cache/imageNotDeployed')
    for i in range(len(newList)):
        if i == 0: cacheImage(binPath, newList[i], mode='w+')
        else: cacheImage(binPath, newList[i], mode='a+')