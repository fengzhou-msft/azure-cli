# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.log import get_logger

logger = get_logger(__name__)


def rest_call(cmd, url, method=None, headers=None, uri_parameters=None,
              body=None, skip_authorization_header=False, resource=None, output_file=None):
    from azure.cli.core.util import send_raw_request
    r = send_raw_request(cmd.cli_ctx, method, url, headers, uri_parameters, body,
                         skip_authorization_header, resource, output_file)
    if not output_file and r.content:
        try:
            return r.json()
        except ValueError:
            logger.warning('Not a json response, outputting to stdout. For binary data '
                           'suggest use "--output-file" to write to a file')
            print(r.text)
    return None


def show_version(cmd):  # pylint: disable=unused-argument
    from azure.cli.core.util import get_az_version_json
    versions = get_az_version_json()
    return versions


def _get_daemon():
    import os
    from azure.cli.core.api import get_config_dir
    from azure.cli.command_modules.util.azdaemon import AzDaemon
    pidfile = os.path.join(get_config_dir(), "azdaemon.pid")
    print(pidfile)
    return AzDaemon(pidfile=pidfile)


def start_daemon(cmd):
    d = _get_daemon()
    logger.warning("Start Daemon.")
    d.start()


def stop_daemon(cmd):
    d = _get_daemon()
    d.stop()
    logger.warning("Daemon stopped!")


def restart_daemon(cmd):
    d = _get_daemon()
    logger.warning("Restart Daemon.")
    d.restart()
