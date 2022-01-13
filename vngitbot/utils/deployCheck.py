from kubernetes import client, config
from utils import cacheImage
import time, os

def readCache(imageName):
    listCache = []
    with open(imageName, 'r') as f:
        lines = f.read().splitlines()
        # for l in lines: listCache.append(l.split(','))
        for l in lines: listCache.append(l)
    return listCache


def isDeployed(image, kubeconfig):
    config.load_kube_config(config_file=kubeconfig)
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    # startedTime = p.status.container_statuses[0].state.running
    for p in ret.items:
        if image in p.spec.containers[0].image: return(True, p)
    return(False, None)


def verifySuccess(pod, kubeconfig):
    config.load_kube_config(config_file=kubeconfig)
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    check = 0
    while check < 3:
        if pod.status.container_statuses[0].state.running != None: return True
        time.sleep(3)
        check += 1
    if check == 3: return False


def removeCachedImage(binPath, cachedImage, listCache):
    newList = listCache
    newList.remove(cachedImage)
    for i in range(len(newList)):
        if i == 0: cachedImage(binPath, newList[i][0], mode='w')
        else: cachedImage(binPath, newList[i][0], mode='a')

