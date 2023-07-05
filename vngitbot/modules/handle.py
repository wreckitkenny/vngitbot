from utils import BasicConfig
from .changeImageTag import ChangeTag
import json, logging

class Handle:
    def __init__(self):
        bc = BasicConfig()
        self.binPath = bc.binPath
        self.parser = bc.parser
        bc.logConfig()

    def handle(self, post_data, path):
        if path == '/':
            logging.info("[{}]".format(post_data.decode("utf-8")))
            eventType = json.loads(post_data)['type']
            resource = json.loads(post_data)['event_data']['resources'][0]['resource_url']
            if eventType == "PUSH_ARTIFACT":
                logging.info("-"*100)
                ChangeTag().changeImageTag(resource)

        # if path == '/verify':
        #     logging.debug("[{}]".format(post_data))
        #     kind = json.loads(post_data)['object_kind']
        #     status = json.loads(post_data)['object_attributes']['status']
        #     commitMsg = json.loads(post_data)['commit']['message']
        #     project = json.loads(post_data)['project']['name']
        #     namespace = json.loads(post_data)['project']['namespace']
        #     if kind == "pipeline" and status == "success":
        #         CheckDeploy().checkDeploy()
        #     if kind == "pipeline" and status == "failed":
        #         Telegram().notifyPipelineFailure(namespace, project, commitMsg)