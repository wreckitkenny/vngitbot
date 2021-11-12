import os, logging, re, gitlab, pickle, yaml

# def cacheOwner(binPath, owners, branchName):
#     if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
#     with open(binPath+'/.cache/'+branchName, 'w') as f:
#         for o in owners: f.write(str(o) + '\n')
def downloadOwnerFile(binPath, cdFolder, cdProject, branchName):
    logging.debug("Gitbot is caching OWNERS file.")
    if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
    with open(binPath+'/.cache/'+branchName, 'wb') as f:
        cdProject.files.raw(file_path=cdFolder+'/OWNERS', ref='master', streamed=True, action=f.write)

def cacheProject(binPath, cdProject, branchName):
    logging.debug("Gitbot is caching ProjectID object.")
    if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
    with open(binPath+'/.cache/.'+branchName, 'wb') as f:
        pickle.dump(cdProject, f)

def changeContent(file, old, new):
    with open(file, 'r') as f:
        content = f.read()
        content = content.replace(old, new)
    with open(file, 'w') as f:
        f.write(content)

def changeTag(gl, resource, cdProject, oldTag, newTag, binPath, location, branchName, botname):
    # Check directory existing
    cdFolder = '/'.join(location[0].split('/')[:-1])
    if os.path.isdir(binPath+'/'+cdFolder) == False: os.makedirs(binPath+'/'+cdFolder)

    # Download raw file
    logging.info("Gitbot is downloading CD file containing tag [{}].".format(oldTag))
    with open(binPath+'/'+location[0], 'wb') as f:
        cdProject.files.raw(file_path=location[0].strip(), ref='master', streamed=True, action=f.write)

    # Change content
    logging.info("Gitbot is changing tag from old tag [{}] to new tag [{}].".format(oldTag, newTag))
    changeContent(binPath+'/'+location[0], oldTag, newTag)

    # Commit changes
    data = {
        'branch': branchName,
        'commit_message': 'Change tag',
        'actions': [
            {
                'action': 'update',
                'file_path': location[0].strip(),
                'content': open(binPath+'/'+location[0]).read(),
            }
        ]
    }
    logging.info('Gitbot is committing new change to branch [{}].'.format(branchName))
    cdProject.commits.create(data)

    # Create merge request
    if branchName == newTag:
        # owners = getApprovers(gl, cdProject, cdFolder)
        downloadOwnerFile(binPath, cdFolder, cdProject, branchName)
        # cacheProject(binPath, cdProject, branchName)
        botId = [gl.users.list(username=botname)[0].id]
        logging.info('Gitbot is creating a merge request for new branch [{}]'.format(branchName))
        mr = cdProject.mergerequests.create({'source_branch':branchName, 'target_branch':'master', 'title':'Vnpaybot has released {}'.format(resource), 'assignee_ids':botId})
        mr.approval_rules.create({"name": "Production MR Policy", "approvals_required": 2, "rule_type": "regular","user_ids": botId})

    # Complete
    logging.info('Gitbot has finished changing old tag [{}] to new tag [{}].'.format(oldTag, newTag))


def checkMergeRole(cachePath, username):
    with open(cachePath, 'r') as f: 
        owners = yaml.load(f, Loader=yaml.FullLoader)
        merges = owners['merge']
        if username in merges: return True
        

def checkLeftApproval(cachePath):
    with open(cachePath, 'r') as f: 
        owners = yaml.load(f, Loader=yaml.FullLoader)
        approvals = owners['approve']
    if len(approvals) == 0:
        return True


def checkEnvironment(gl, parser, pushedTag):
    env = cdProject = ''
    id_dev = parser.get('WORKLOAD', 'DEV_DEPLOYMENT')
    id_staging = parser.get('WORKLOAD', 'STAGING_DEPLOYMENT')
    id_prod = parser.get('WORKLOAD', 'PROD_DEPLOYMENT')
    if pushedTag.split('-')[0] == 'd' and checkProjectID(gl, id_dev) == 1: 
        env = 'dev'
        cdProject = gl.projects.get(id_dev)
    # elif re.match('(v)?((\d\.){2}\d)', pushedTag.split('-')[0]) != None and checkProjectID(gl, id_staging) == 1:
    if pushedTag.split('-')[0] == 't' and checkProjectID(gl, id_staging) == 1:
        env = 'test'
        cdProject = gl.projects.get(id_staging)
    if pushedTag.split('-')[0] == 'm' and checkProjectID(gl, id_prod) == 1:
        env = 'prod'
        cdProject = gl.projects.get(id_prod)
    return(env,cdProject)

def checkProjectID(gl, id):
    try:
        gl.projects.get(id)
    except gitlab.exceptions.GitlabGetError:
        logging.error("ProjectID {} is not existing.".format(id))
        return 0
    return 1


# def getApprovers(gl, cdProject, cdFolder):
#     try:
#         owners = cdProject.files.raw(file_path=cdFolder+"/OWNERS", ref='master')
#         try:
#             assignees = [o for o in owners.decode().strip().split('\n')]
#             assignee_id = [gl.users.list(username=assignee)[0].id for assignee in assignees]
#             return assignee_id
#         except IndexError:
#             logging.error("OWNERS file is empty")
#             return []
#     except gitlab.exceptions.GitlabGetError:
#         logging.error("OWNERS file is not found.")
#         return []
    
def enableProxy(proxy):
    os.environ['http_proxy'] = proxy 
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    
def getOldTag(cdProject, repoName):
    try:
        files = cdProject.repository_tree(recursive=True, all=True)
        for file in files:
            if file['type'] == 'blob':
                file_content = cdProject.files.raw(file_path=file['path'], ref='master')
                if repoName in str(file_content):
                    for i in file_content.decode().split('\n'):
                        #if 'image' in i: return i.split(':')[-1].strip()
                        ### Code on Cloud
                        if 'tag' in i:
                            i = re.sub(r'[\n\t ]', '', i)
                            #Oldest i = re.search('(?<=:)(v)?(((\d(\.\d)+)-)?([a-z0-9]+)|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            #Older i = re.search('(?<=:)(v)?(((\d(\.\d)+)-)|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            i = re.search('(?<=:)(m-)?(v)?((\d\.){2}\d-|[a-z]-)?([a-z0-9]+)',re.sub(r'[\n\t ]', '', i))
                            return i.group(0)
        logging.error("Repository [{}] is not found.".format(repoName))
        return ''
    except gitlab.exceptions.GitlabGetError:
        logging.error("CD repository is empty or not initialized yet.")


def filterEmpty(_list):
    filter_object = filter(lambda x: x != "", _list)
    without_empty_strings = list(filter_object)   
    return without_empty_strings

def makeComment(binPath, sBranch, mrId, note):
    logging.debug("Gitbot is making a comment.")
    with open(binPath+'/.cache/.'+sBranch, 'rb') as f:
        cdProj = pickle.load(f)
    mr = cdProj.mergerequests.get(mrId)
    mr.notes.create({'body': note})


# def logConfig(parser):
#     level = parser.get('LOG', 'LOG_LEVEL')
#     if level == 'INFO': lvl = logging.INFO
#     if level == 'DEBUG': lvl = logging.DEBUG
#     logging.basicConfig(filename=parser.get('LOG', 'LOG_PATH')+'/'+parser.get('LOG', 'LOG_FILENAME'), 
#                         level=lvl,
#                         format='%(asctime)s | %(levelname)s | %(message)s',
#                         datefmt='%d/%m/%Y | %I:%M:%S')


def pullOwners(binPath, sBranch, cachePath, username, mrId):
    with open(cachePath, 'r') as f: 
        owners = yaml.load(f, Loader=yaml.FullLoader)
        approvals = owners['approve']
    if len(approvals) != 0:
        if username in approvals:
            logging.debug('Username [{}] is authorized to approve'.format(username))
            approvals.remove(username)
            owners['approve'] = approvals
            with open(cachePath, 'w') as f:
                logging.debug('Gitbot is updating cached MR policy.')
                yaml.dump(owners, f)
        else: 
            makeComment(binPath, sBranch, mrId, note='[__Warning__] User [@{}] is not authorized to approve the merge request.'.format(username))
            logging.debug("User [{}] is not authorized to approve the merge request.".format(username))
        
    isEmpty = checkLeftApproval(cachePath)
    if isEmpty == True:
        logging.debug("Gitbot is triggering a comment for merging the request {}.".format(mrId))
        with open(cachePath, 'r') as f: merges = yaml.load(f, Loader=yaml.FullLoader)['merge']
        for m in merges: makeComment(binPath, sBranch, mrId, note='Type "merge" to merge. [@{}]'.format(m))


def pushOwners(cachePath, username):
    with open(cachePath, 'r') as f: 
        owners = yaml.load(f, Loader=yaml.FullLoader)
        approvals = owners['approve']
    if username not in approvals:
        approvals.append(username)
        owners['approve'] = approvals
        with open(cachePath, 'w') as f:
            logging.debug('Gitbot is updating cached MR policy.')
            yaml.dump(owners, f)
    else: 
        logging.debug("User [{}] is existing.".format(username))
    

def sanitize(binPath, sBranch):
    logging.debug("Gitbot is sanitizing {}".format(binPath+'/.cache/'+sBranch))
    os.remove(binPath+'/.cache/'+sBranch)
    logging.debug("Gitbot is sanitizing {}".format(binPath+'/.cache/.'+sBranch))
    os.remove(binPath+'/.cache/.'+sBranch)


def searchFile(cdProject, repoName):
    fileList = []
    files = cdProject.repository_tree(recursive=True, all=True)
    for file in files:
        if file['type'] == 'blob':
            file_content = cdProject.files.raw(file_path=file['path'], ref='master')
            if repoName in str(file_content):
                fileList.append(file['path'])
    return fileList
