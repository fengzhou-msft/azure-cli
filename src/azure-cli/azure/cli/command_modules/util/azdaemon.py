import time
from daemons.prefab import run

class AzDaemon(run.RunDaemon):

    def run(self):
        while True:
            self.update_ext_cmd_index()
            self.update_latest_version()
            time.sleep(300)
    
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
            from distutils.version import LooseVersion  # pylint: disable=import-error,no-name-in-module
            version_dict = versions['azure-cli']
            local = version_dict['local']
            pypi = version_dict.get('pypi', None)
            if pypi and LooseVersion(pypi) > LooseVersion(local):
                from azure.cli.command_modules.util.custom import upgrade_version
                print("start upgrade to version:{}".format(pypi))
                upgrade_version()
