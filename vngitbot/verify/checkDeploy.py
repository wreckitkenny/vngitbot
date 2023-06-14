from utils import BasicConfig, readCache, isDeployed, verifySuccess, removeCachedImage
from telegram import Telegram
import logging, time
import functools

class CheckDeploy:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.binPath = bc.binPath
        self.cacheDir = self.parser.get('GENERAL', 'CACHE_DIR')
        self.kubeconfig = self.parser.get('K8S', 'KUBE_CONFIG')
        bc.logConfig()

    @functools.lru_cache(maxsize=128)
    def checkDeploy(self):
        isSucceeded = None
        isDeployedOnK8s = None
        failedCount = 0

        logging.info("Vngitbot is reading image caches.")
        listCache = readCache(self.cacheDir+'/imageNotDeployed')
        listCache.reverse()

        for cachedImage in listCache:
            logging.info("Vngitbot is checking [{}]".format(cachedImage))
            isDeployedOnK8s = isDeployed(cachedImage, self.kubeconfig)

            if isDeployedOnK8s == True:
                logging.info("Vngitbot is checking the service.")
                while 1:
                    checkSuccess = verifySuccess(cachedImage, self.kubeconfig)
                    isSucceeded, namespace, startedTime = checkSuccess[0], checkSuccess[1], checkSuccess[2]
                    if isSucceeded == True: break
                    if failedCount == 30: break
                    if isSucceeded == False:
                        failedCount += 1
                        if len(str(failedCount)) > 1 and str(failedCount).endswith('0'):
                            logging.info(">> Successfull to deploy? {}".format(isSucceeded))
                            logging.info(">> Image {} is not found to verify. Retrying...{}/3".format(cachedImage, failedCount//10))
                        time.sleep(3)

            logging.info("Vngitbot is notifying Telegram group.")
            if isSucceeded == True:
                Telegram().notifySuccess(cachedImage, namespace, startedTime)
            if isSucceeded == False:
                Telegram().notifyFailure(cachedImage, namespace)

            logging.info("Vngitbot is removing the cached image.")
            removeCachedImage(self.binPath, cachedImage, listCache)



    # def checkDeploy(self):
    #     isSucceeded = None
    #     listCache = readCache(self.cacheDir+'/imageNotDeployed')
    #     listCache.reverse()
    #     logging.info("Vngitbot is checking the deployment....")
    #     for cachedImage in listCache:
    #         isDeployedOnK8s = isDeployed(cachedImage, self.kubeconfig)
    #         if isDeployedOnK8s == True:
    #             logging.info("Deployed. Checking the service if running....")
    #             isSucceeded, startedTimeOrReason = verifySuccess(cachedImage, self.kubeconfig)
    #         if isSucceeded == True:
    #             logging.info("Notifying Telegram group....")
    #             Telegram().notifySuccess(cachedImage, startedTimeOrReason)
    #             logging.info("Removing the cached image....")
    #             removeCachedImage(self.binPath, cachedImage, listCache)
    #         # if isSucceeded == False:
    #         #     Telegram().notifyFailure(cachedImage, startedTimeOrReason)
    #         if isSucceeded == False:
    #             Telegram().notifyFailure(cachedImage)