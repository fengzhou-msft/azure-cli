import time
from daemons.prefab import run

class AzDaemon(run.RunDaemon):

    def run(self):
        while True:
            self.update_ext_cmd_index()
            self.update_latest_version()
            time.sleep(60)
    
    def update_ext_cmd_index(self):
        pass

    def update_latest_version(self):
        import os
        import datetime
        from azure.cli.core._environment import get_config_dir
        from azure.cli.core._session import VERSIONS
        from azure.cli.core.util import _get_local_versions, _update_latest_from_pypi, _VERSION_UPDATE_TIME

        versions = _get_local_versions()

        VERSIONS.load(os.path.join(get_config_dir(), 'versionCheck.json'))
        versions, success = _update_latest_from_pypi(versions)
        if success:
            VERSIONS['versions'] = versions
            VERSIONS[_VERSION_UPDATE_TIME] = str(datetime.datetime.now())