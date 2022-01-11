from utils import BasicConfig, readCache, isDeployed, verifySuccess, removeCachedImage
from telegram import Telegram

class CheckDeploy:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.binPath = bc.binPath
        self.cacheDir = self.parser.get('GENERAL', 'CACHE_DIR')
        self.kubeconfig = self.parser.get('K8S', 'KUBE_CONFIG')


    def checkDeploy(self):
        listCache = readCache(self.cacheDir+'/imageNotDeployed')
        for cachedImage in listCache:
            isDeployedOnK8s, _pod = isDeployed(cachedImage[0], self.kubeconfig)
            if isDeployedOnK8s == True: isSucceeded = verifySuccess(_pod, self.kubeconfig)
            if isSucceeded == True:
                Telegram().notifySuccess(cachedImage[0])
                removeCachedImage(self.binPath, cachedImage, listCache)