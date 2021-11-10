from _common import *
from _features import *
import json, logging

class Handle:
    def __init__(self):
        self.binPath = bc.binPath
        bc.logConfig(self.parser)

    def handle(self, post_data, path):
        if path == '/':
                eventType = json.loads(post_data)['type']
                resource = json.loads(post_data)['event_data']['resources'][0]['resource_url']
                if eventType == "PUSH_ARTIFACT":  
                    logging.info("-"*100)
                    ChangeTag.changeImageTag(resource, self.binPath)
        if path == '/merge':
            eventType = json.loads(post_data)['event_type']
            username = json.loads(post_data)['user']['username']
            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'approved':
                mrId = json.loads(post_data)['object_attributes']['iid']
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                CheckApproval.checkApproval(bc.binPath, mrId, sBranch, username)
            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'open':
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                lastCommit = json.loads(post_data)['object_attributes']['last_commit']['id']
                userMadeMR = json.loads(post_data)['user']['username']
                projectId = json.loads(post_data)['project']['id']
                CacheManualMR.cacheManualMR(bc.binPath, bc.configPath, projectId, lastCommit, sBranch, userMadeMR)

            if eventType == "note" and json.loads(post_data)['object_attributes']['note'] == 'merge':
                sBranch = json.loads(post_data)['merge_request']['source_branch']
                mrId = json.loads(post_data)['merge_request']['iid']
                MakeMerge.makeMerge(bc.binPath, username, sBranch, mrId)