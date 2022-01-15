from utils import BasicConfig, readCache, isDeployed, verifySuccess, removeCachedImage
from telegram import Telegram
import logging

class CheckDeploy:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.binPath = bc.binPath
        self.cacheDir = self.parser.get('GENERAL', 'CACHE_DIR')
        self.kubeconfig = self.parser.get('K8S', 'KUBE_CONFIG')
        bc.logConfig()


    def checkDeploy(self):
        listCache = readCache(self.cacheDir+'/imageNotDeployed')
        isSucceeded = None
        for cachedImage in listCache:
            logging.info("Checking the deployment....")
            isDeployedOnK8s, _pod = isDeployed(cachedImage, self.kubeconfig)
            if isDeployedOnK8s == True:
                logging.info("Deployed. Checking the service if running....")
                isSucceeded, startedTimeOrReason = verifySuccess(cachedImage, _pod, self.kubeconfig)
            if isSucceeded == True:
                logging.info("Notifying Telegram group....")
                Telegram().notifySuccess(cachedImage, startedTimeOrReason)
                logging.info("Removing the cached image....")
                removeCachedImage(self.binPath, cachedImage, listCache)
            # if isSucceeded == False:
            #     Telegram().notifyFailure(cachedImage, startedTimeOrReason)
            if isSucceeded == False:
                Telegram().notifyFailure(cachedImage)