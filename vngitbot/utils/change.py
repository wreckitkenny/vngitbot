import os, logging, re, gitlab
from weakref import ref

def checkEnvironment(gl, parser, pushedTag):
    env = cdProject = ''
    id_dev = parser.get('WORKLOAD', 'DEV_DEPLOYMENT')
    id_staging = parser.get('WORKLOAD', 'STAGING_DEPLOYMENT')
    id_prod = parser.get('WORKLOAD', 'PROD_DEPLOYMENT')
    if pushedTag.split('-')[0] == 'd' and checkProjectID(gl, id_dev) == 1:
        env = 'dev'
        cdProject = gl.projects.get(id_dev)
    if pushedTag.split('-')[0] == 't' and checkProjectID(gl, id_staging) == 1:
        env = 'test'
        cdProject = gl.projects.get(id_staging)
    if pushedTag.split('-')[0] == 'm' and checkProjectID(gl, id_prod) == 1:
        env = 'prod'
        cdProject = gl.projects.get(id_prod)
    return(env,cdProject)

def checkDup(cdProject, repoName, location):
    notDupList = []
    for path in location:
        fileContent = cdProject.files.raw(file_path=path, ref='master')
        repoNotDup = [re.search('(?<=repository:)([a-z]+.)+[a-z]+(\/[a-zA-Z0-9-_]+)+',re.sub(r'[\n\t ]', '', x)).group(0) for x in fileContent.decode("utf-8").split("\n") if 'repository:' in x]
        if repoNotDup[0] == repoName: notDupList.append(path)
    return notDupList


def getOldTag(cdProject, valuePathList, repoName):
    tagList = []
    for valuePath in valuePathList:
        cdFile = cdProject.files.raw(file_path=valuePath, ref='master')
        tag = [re.search('(?<=tag:)(m-)?(v)?(((\d+\.){2}\d+)?(-)?)?([a-zA-Z0-9]+-)?([a-zA-Z0-9]+)?',re.sub(r'[\n\t ]', '', x)).group(0) for x in cdFile.decode("utf-8").split("\n") if 'tag:' in x]
        if tag[0] not in tagList: tagList.append(tag[0])
    if len(tagList) > 1:
        logging.error("Different version tags found.")
        return ''
    return tagList[0]


# def searchFile(cdProject, repoName):
#     valuePathList = []
#     files = cdProject.repository_tree(recursive=True, all=True)
#     for file in files:
#         if file['type'] == 'blob':
#             file_content = cdProject.files.raw(file_path=file['path'], ref='master')
#             if repoName in str(file_content): valuePathList.append(file['path'])
#     if len(valuePathList) > 1: valuePathList = checkDup(cdProject, repoName, valuePathList)
#     return(valuePathList)

def locateBlob(cdProject, repoName):
    listOfBlobName = []
    blobList = cdProject.search(gitlab.const.SearchScope.BLOBS, repoName)
    for blob in blobList: listOfBlobName.append(blob["filename"])
    if len(listOfBlobName) > 1: listOfBlobName = checkDup(cdProject,repoName,listOfBlobName)
    return listOfBlobName


def changeTag(gl, resource, cdProject, oldTag, newTag, binPath, blobList, branchName, botname, repoName):
    for blob in blobList:
        # Check directory existing
        cdFolder = '/'.join(blob.split('/')[:-1])
        if os.path.isdir(binPath+'/'+cdFolder) == False: os.makedirs(binPath+'/'+cdFolder)

        # Download raw file
        logging.info("Vngitbot is downloading CD file containing tag [{}].".format(oldTag))
        with open(binPath+'/'+blob, 'wb') as f:
            cdProject.files.raw(file_path=blob.strip(), ref='master', streamed=True, action=f.write)

        # Change content
        logging.info("Vngitbot is changing tag from old tag [{}] to new tag [{}].".format(oldTag, newTag))
        changeContent(binPath+'/'+blob, oldTag, newTag)

        # Commit change
        data = {
            'branch': branchName,
            'commit_message': 'Change tag for {} from oldtag {} to newtag {}'.format(resource.split(':')[0], oldTag, newTag),
            'actions': [
                {
                    'action': 'update',
                    'file_path': blob.strip(),
                    'content': open(binPath+'/'+blob).read(),
                }
            ]
        }
        logging.info('Vngitbot is committing new change to branch [{}].'.format(branchName))
        cdProject.commits.create(data)

    # Create merge request
    if branchName != "master":
        botId = [gl.users.list(username=botname)[0].id]
        logging.info('Gitbot is creating a merge request for new branch [{}]'.format(branchName))
        mr = cdProject.mergerequests.create({'source_branch':branchName, 'target_branch':'master', 'title':'Vnpaybot has released {}'.format(resource), 'assignee_ids':botId})
        mr.approval_rules.create({"name": "Production MR Policy", "approvals_required": 2, "rule_type": "regular","user_ids": botId})

    # # Cache image for deployment
    # cacheImage(binPath, resource, mode='a+')

    # Complete
    logging.info('Vngitbot has finished changing old tag [{}] to new tag [{}].'.format(oldTag, newTag))


def changeContent(file, old, new):
    with open(file, 'r') as f:
        content = f.read()
        content = content.replace(old, new)
    with open(file, 'w') as f:
        f.write(content)


def checkProjectID(gl, id):
    try:
        gl.projects.get(id)
    except gitlab.exceptions.GitlabGetError:
        logging.error("ProjectID {} is not existing.".format(id))
        return 0
    return 1

# def cacheImage (binPath, imageName, mode):
#     if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
#     with open(binPath+'/.cache/imageNotDeployed', mode) as f:
#         f.seek(0)
#         data = f.read(100)
#         if len(data) > 0 :
#             f.write("\n")
#         f.write(imageName)