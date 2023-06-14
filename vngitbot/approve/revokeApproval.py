from utils import BasicConfig, pushOwners
import logging, os

class RevokeApproval:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.gl = bc.gl
        self.binPath = bc.binPath
        bc.logConfig()

    def revokeApproval(self, mrId, sBranch, username):
        logging.info("An approval is revoked.")
        cacheExisting = os.path.isfile(self.binPath+'/.cache/'+sBranch)
        if cacheExisting == True: pushOwners(self.binPath+'/.cache/'+sBranch, username)
        else: logging.error("Cached file {} is not existing.".format(self.binPath+'/.cache/'+sBranch))