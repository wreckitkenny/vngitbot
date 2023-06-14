from utils import BasicConfig, checkLeftApproval, checkMergeRole, makeComment, sanitize
import logging, pickle

class MakeMerge:
    def __init__(self):
        bc = BasicConfig()
        self.gl = bc.gl
        self.binPath = bc.binPath
        bc.logConfig()

    def makeMerge(self, username, sBranch, mrId):
        isEmpty = checkLeftApproval(self.binPath+'/.cache/'+sBranch)
        allowToMerge = checkMergeRole(self.binPath+'/.cache/'+sBranch, username)
        if allowToMerge != True:
            logging.info('User [{}] is not authorized to merge the request.'.format(username))
            makeComment(self.binPath, sBranch, mrId, note='[__Warning__] User [@{}] is not authorized to merge the request.'.format(username))
        if allowToMerge == True and isEmpty != True:
            logging.info('There is not enough approval to merge.')
            makeComment(self.binPath, sBranch, mrId, note='[__Warning__] There is not enough approval to merge.')
        if allowToMerge == True and isEmpty == True:
            logging.info('User [{}] is merging the request.'.format(username))
            with open(self.binPath+'/.cache/.'+sBranch, 'rb') as f: cdProj = pickle.load(f)
            mr = cdProj.mergerequests.get(mrId)
            mr.merge()
            logging.info("Vngitbot is sanitizing caches.")
            sanitize(self.binPath, sBranch)