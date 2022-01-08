from utils import *
from telegram import notifyTagChange
import logging

class ChangeTag:
    def __init__(self):
        bc = BasicConfig()
        self.parser = bc.parser
        self.gl = bc.gl
        self.binPath = bc.binPath
        bc.logConfig()

    def changeImageTag(self, resource):
        # Variables definition
        global workPath, cdProject
        branchName = 'master'
        repoName = resource.split(':')[0]
        newTag = resource.split(':')[1]
        cluster = self.parser.get('GENERAL', 'CLUSTER')
        botname = self.parser.get('GITLAB', 'GITLAB_BOTNAME')
        proxy = self.parser.get('PROXY','ENABLED')
        proxyInfo = self.parser.get('PROXY','PROXY_ADDRESS')

        logging.info("Gitbot is proceeding new image [{}]".format(resource))
        env, cdProject = checkEnvironment(self.gl, self.parser, newTag)
        if env != '':
            oldTag = getOldTag(cdProject, repoName)
            location = searchFile(cdProject, repoName)
            branch_list = [branch.name for branch in cdProject.branches.list()]

            if env == 'prod':
                if newTag in branch_list:
                    logging.warning('Branch [{}] is existing.'.format(newTag))
                    cdProject.branches.delete(newTag)
                    logging.info('Gitbot has removed old [{}] branch'.format(newTag))
                logging.info('Gitbot is creating a new [{}] branch'.format(newTag))
                cdProject.branches.create({'branch': newTag, 'ref': 'master'})
                branchName = newTag

            if oldTag != '':
                logging.info('GitBot is comparing old tag [{}] to new tag [{}].'.format(oldTag, newTag))
                if (lambda x,y: (x>y)-(x<y))(oldTag,newTag) == 0: logging.info("==> No tag changed!!!")
                else:
                    changeTag(self.gl, resource, cdProject, oldTag, newTag, self.binPath, location, branchName, botname)
                    # notifyTagChange(oldTag, newTag, cluster, env, repoName, proxy, proxyInfo, token=self.parser.get('SLACK', 'SLACK_TOKEN'),
                    #             channel=self.parser.get('SLACK', 'SLACK_CHANNEL'),
                    #             app=self.parser.get('SLACK', 'SLACK_APP'))
                    notifyTagChange(oldTag, newTag, cluster, env, repoName, proxy, proxyInfo,
                                    token=self.parser.get('TELEGRAM', 'TELEGRAM_TOKEN'),
                                    channel=self.parser.get('TELEGRAM', 'TELEGRAM_CHANNEL'))
        else: logging.error("==> The image [{}] is rejected to deploy.".format(resource))