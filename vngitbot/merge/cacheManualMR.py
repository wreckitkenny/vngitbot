from utils import BasicConfig, downloadOwnerFile, cacheProject

class CacheManualMR:
    def __init__(self):
        bc = BasicConfig()
        self.gl = bc.gl
        self.binPath = bc.binPath
        bc.logConfig()

    def cacheManualMR(self, projectId, lastCommit, sBranch):
        projectId = self.gl.projects.get(projectId)
        commit = projectId.commits.get(lastCommit[:8])
        diffInfo = commit.diff()
        path = '/'.join(diffInfo[0]['old_path'].split('/')[:-1])
        downloadOwnerFile(self.binPath, path, projectId, sBranch)
        cacheProject(self.binPath, projectId, sBranch)