import logging, yaml
from .merge import makeComment, checkLeftApproval


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
        logging.debug("Vngitbot is triggering a comment for merging the request {}.".format(mrId))
        with open(cachePath, 'r') as f: merges = yaml.load(f, Loader=yaml.FullLoader)['merge']


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