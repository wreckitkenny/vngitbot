from utils import BasicConfig, pullOwners
import logging, os

class CheckApproval:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.gl = bc.gl
        self.binPath = bc.binPath
        bc.logConfig()

    def checkApproval(self, mrId, sBranch, username):
        logging.info("A new approval is triggered.")
        cacheExisting = os.path.isfile(self.binPath+'/.cache/'+sBranch)
        if cacheExisting == True:
            logging.info("Vngitbot is checking if username [{}] is authorized to approve.".format(username))
            pullOwners(self.binPath, sBranch, self.binPath+'/.cache/'+sBranch, username, mrId)
        else: logging.error("Cached file {} is not existing.".format(self.binPath+'/.cache/'+sBranch))