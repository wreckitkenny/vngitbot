from utils import BasicConfig, checkEnvironment, searchFile, getOldTag, changeTag, sanitize
from .telegram import Telegram
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
        botname = self.parser.get('GITLAB', 'GITLAB_BOTNAME')

        logging.info("Vngitbot is proceeding new image [{}]".format(resource))
        env, cdProject = checkEnvironment(self.gl, self.parser, newTag)

        if env != '':
            # valuePathList, namespaceList = searchFile(cdProject, repoName)
            valuePathList = searchFile(cdProject, repoName)
            oldTag = getOldTag(cdProject, valuePathList, repoName)
            branch_list = [branch.name for branch in cdProject.branches.list(all=True)]

            if env == 'prod':
                oldBranch = "{}-{}".format(repoName.split('/')[-1],oldTag)
                if oldBranch in branch_list: cdProject.branches.delete(oldBranch)
                newBranch = "{}-{}".format(repoName.split('/')[-1],newTag)
                logging.info('Vngitbot is creating a new branch - [{}]'.format(newBranch))
                cdProject.branches.create({'branch': newBranch, 'ref': 'master'})
                branchName = newBranch

            if oldTag != '':
                logging.info('Vngitbot is comparing old tag [{}] to new tag [{}].'.format(oldTag, newTag))
                if (lambda x,y: (x>y)-(x<y))(oldTag,newTag) == 0: logging.info("==> No tag changed!!!")
                else:
                    # Change Image tag for an updated repository
                    for location in valuePathList: changeTag(self.gl, resource, cdProject, oldTag, newTag, self.binPath, location, branchName, botname, repoName)
                    # Send an alert to Telegram channels
                    Telegram().notifyTagChange(oldTag, newTag, env, repoName)
        else: logging.error("==> The image [{}] is rejected to deploy.".format(resource))