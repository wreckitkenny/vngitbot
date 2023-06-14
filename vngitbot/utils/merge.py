import os, logging, gitlab, pickle, yaml

def downloadOwnerFile(binPath, cdFolder, cdProject, branchName):
    logging.debug("Vngitbot is caching OWNERS file.")
    if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
    try:
        with open(binPath+'/.cache/'+branchName, 'wb') as f:
            cdProject.files.raw(file_path=cdFolder+'/OWNERS', ref='master', streamed=True, action=f.write)
    except gitlab.exceptions.GitlabGetError:
        logging.error("OWNERS file is not found.")


def cacheProject(binPath, cdProject, branchName):
    logging.debug("Vngitbot is caching ProjectID object.")
    if os.path.isdir(binPath+'/.cache') == False: os.makedirs(binPath+'/.cache')
    with open(binPath+'/.cache/.'+branchName, 'wb') as f:
        pickle.dump(cdProject, f)


def checkLeftApproval(cachePath):
    with open(cachePath, 'r') as f:
        owners = yaml.load(f, Loader=yaml.FullLoader)
        approvals = owners['approve']
    if len(approvals) == 0: return True


def checkMergeRole(cachePath, username):
    with open(cachePath, 'r') as f:
        owners = yaml.load(f, Loader=yaml.FullLoader)
        merges = owners['merge']
        if username in merges: return True


def makeComment(binPath, sBranch, mrId, note):
    logging.debug("Vngitbot is making a comment.")
    with open(binPath+'/.cache/.'+sBranch, 'rb') as f:
        cdProj = pickle.load(f)
    mr = cdProj.mergerequests.get(mrId)
    mr.notes.create({'body': note})


def sanitize(binPath, sBranch):
    logging.debug("Vngitbot is sanitizing {}".format(binPath+'/.cache/'+sBranch))
    os.remove(binPath+'/.cache/'+sBranch)
    logging.debug("Vngitbot is sanitizing {}".format(binPath+'/.cache/.'+sBranch))
    os.remove(binPath+'/.cache/.'+sBranch)


