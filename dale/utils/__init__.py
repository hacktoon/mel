import os
import requests
import logging


def read_file(path):
    with open(path, 'r') as file_obj:
        return file_obj.read()


def read_environment(name, default=''):
    return os.environ.get(name, default)


def request_url(url, default='', timeout=5):
    logging.basicConfig(format='%(levelname)s! %(message)s')
    try:
        r = requests.get(url, allow_redirects=True, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.HTTPError as e:
        logging.warning('HTTP error requesting {!r}'.format(url))
    except requests.Timeout as e:
        logging.warning('Timeout requesting {!r} in {}s'.format(url, timeout))
    except requests.TooManyRedirects as e:
        logging.warning('Too many redirects requesting {!r}'.format(url))
    except requests.ConnectionError as e:
        logging.warning('Name or service not known: {!r}'.format(url))
    except requests.RequestException as e:
        logging.warning("Failed requesting {!r}: {}".format(url, e))
    return default
