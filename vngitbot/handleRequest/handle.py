from utils import BasicConfig, sanitize
from handleRequest import ChangeTag
from approve import CheckApproval, RevokeApproval
from merge import MakeMerge, CacheManualMR
import json, logging

class Handle:
    def __init__(self):
        bc = BasicConfig()
        self.binPath = bc.binPath
        self.parser = bc.parser
        bc.logConfig()

    def handle(self, post_data, path):
        if path == '/':
                eventType = json.loads(post_data)['type']
                resource = json.loads(post_data)['event_data']['resources'][0]['resource_url']
                if eventType == "PUSH_ARTIFACT":
                    logging.info("-"*100)
                    ChangeTag().changeImageTag(resource)
        if path == '/merge':
            eventType = json.loads(post_data)['event_type']
            username = json.loads(post_data)['user']['username']
            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'approved':
                mrId = json.loads(post_data)['object_attributes']['iid']
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                CheckApproval().checkApproval(mrId, sBranch, username)

            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'unapproved':
                mrId = json.loads(post_data)['object_attributes']['iid']
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                RevokeApproval().revokeApproval(mrId, sBranch, username)

            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'open':
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                lastCommit = json.loads(post_data)['object_attributes']['last_commit']['id']
                projectId = json.loads(post_data)['project']['id']
                CacheManualMR().cacheManualMR(projectId, lastCommit, sBranch)

            if eventType == "note" and json.loads(post_data)['object_attributes']['note'] == 'merge':
                sBranch = json.loads(post_data)['merge_request']['source_branch']
                mrId = json.loads(post_data)['merge_request']['iid']
                MakeMerge().makeMerge(username, sBranch, mrId)

            if eventType == "merge_request" and json.loads(post_data)['object_attributes']['action'] == 'merge':
                sBranch = json.loads(post_data)['object_attributes']['source_branch']
                logging.info("Gitbot is sanitizing caches.")
                sanitize(self.binPath, sBranch)