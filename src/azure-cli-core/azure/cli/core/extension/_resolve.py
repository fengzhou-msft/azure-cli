# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from pkg_resources import parse_version

from azure.cli.core.extension import ext_compat_with_cli, WHEEL_INFO_RE
from azure.cli.core.extension._index import get_index_extensions

from knack.log import get_logger
from knack.util import CLIError

logger = get_logger(__name__)

TRIES = 3
AZ_SERVICE_URL = "http://az-service.azurewebsites.net/extension"

class NoExtensionCandidatesError(Exception):
    pass


def _is_not_platform_specific(item):
    parsed_filename = WHEEL_INFO_RE(item['filename'])
    p = parsed_filename.groupdict()
    if p.get('abi') == 'none' and p.get('plat') == 'any':
        return True
    logger.debug("Skipping '%s' as not universal wheel."
                 "We do not currently support platform specific extension detection. "
                 "They can be installed with the full URL %s", item['filename'], item.get('downloadUrl'))
    return False


def _is_compatible_with_cli_version(item):
    is_compatible, cli_core_version, min_required, max_required = ext_compat_with_cli(item['metadata'])
    if is_compatible:
        return True
    logger.debug("Skipping '%s' as not compatible with this version of the CLI. "
                 "Extension compatibility result: is_compatible=%s cli_core_version=%s min_required=%s "
                 "max_required=%s", item['filename'], is_compatible, cli_core_version, min_required, max_required)
    return False


def _is_greater_than_cur_version(cur_version):
    if not cur_version:
        return None
    cur_version_parsed = parse_version(cur_version)

    def filter_func(item):
        item_version = parse_version(item['metadata']['version'])
        if item_version > cur_version_parsed:
            return True
        logger.debug("Skipping '%s' as %s not greater than current version %s", item['filename'],
                     item_version, cur_version_parsed)
        return False
    return filter_func


def resolve_from_index(extension_name, cur_version=None, index_url=None, target_version=None):
    """
    Gets the download Url and digest for the matching extension

    :param cur_version: threshold verssion to filter out extensions.
    """
    candidates = get_extension(extension_name)

    if not candidates:
        raise NoExtensionCandidatesError("No extension found with name '{}'".format(extension_name))

    filters = [_is_not_platform_specific, _is_compatible_with_cli_version, _is_greater_than_cur_version(cur_version)]

    for f in filters:
        logger.debug("Candidates %s", [c['filename'] for c in candidates])
        candidates = list(filter(f, candidates))
    if not candidates:
        raise NoExtensionCandidatesError("No suitable extensions found.")

    candidates_sorted = sorted(candidates, key=lambda c: parse_version(c['metadata']['version']), reverse=True)
    logger.debug("Candidates %s", [c['filename'] for c in candidates_sorted])
    logger.debug("Choosing the latest of the remaining candidates.")

    if target_version:
        try:
            chosen = [c for c in candidates_sorted if c['metadata']['version'] == target_version][0]
        except IndexError:
            raise NoExtensionCandidatesError('Extension with version {} not found'.format(target_version))
    else:
        chosen = candidates_sorted[0]

    logger.debug("Chosen %s", chosen)
    download_url, digest = chosen.get('downloadUrl'), chosen.get('sha256Digest')
    if not download_url:
        raise NoExtensionCandidatesError("No download url found.")
    return download_url, digest


def resolve_project_url_from_index(extension_name):
    """
    Gets the project url of the matching extension from the index
    """
    candidates = get_index_extensions().get(extension_name, [])
    if not candidates:
        raise NoExtensionCandidatesError("No extension found with name '{}'".format(extension_name))
    try:
        return candidates[0]['metadata']['extensions']['python.details']['project_urls']['Home']
    except KeyError as ex:
        logger.debug(ex)
        raise CLIError('Could not find project information for extension {}.'.format(extension_name))


def get_extension(ext_name):
    import requests
    from azure.cli.core.util import should_disable_connection_verify

    for try_number in range(TRIES):
        try:
            response = requests.get('{}?name={}'.format(AZ_SERVICE_URL, ext_name), verify=(not should_disable_connection_verify()))
            if response.status_code == 200:
                return response.json()
            msg = ERR_TMPL_NON_200.format(response.status_code, AZ_SERVICE_URL)
            raise CLIError(msg)
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
            msg = ERR_TMPL_NO_NETWORK.format(str(err))
            raise CLIError(msg)
        except ValueError as err:
            # Indicates that url is not redirecting properly to intended index url, we stop retrying after TRIES calls
            if try_number == TRIES - 1:
                msg = ERR_TMPL_BAD_JSON.format(str(err))
                raise CLIError(msg)
            import time
            time.sleep(0.5)
            continue
  