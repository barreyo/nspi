"""API spec for Nightscout system."""

import time
import logging

from requests import Request, Session

logger = logging.getLogger(__name__)
API_URI_V1 = '/api/v1/'


class NightscoutAPI(object):
    """Docstring for NightscoutAPI."""

    def __init__(self, server_root):
        """
        Construct API object.

        Args:
            server_root: String denoting the server root path.
        """
        self.server_root = server_root
        self.headers = {
            'Accept': 'application/json',
            'Referer': self.server_root,
        }

    def _retry(self, fun, times=3, wait=10):
        """
        Retry a function n number of times with x wait inbetween tries.

        Args:
            fun: Function to run with result.
            times: Number of retries before giving up on the request.
            wait: The number of seconds to wait inbetween each attempt.

        Returns:
            The result of the supplied function.

        Throws:
            Exception if the number of retries are exceeded.
        """
        for x in xrange(times):
            try:
                return fun()
            except Exception:
                if x >= times - 1:
                    raise
                logger.debug('Retrying API request, n=%s', x)
            logger.info('Waiting %ss, before next attempt', wait)
            time.sleep(wait)

    def _get(self, uri, retries=3):
        """
        Do a get request against the API.

        Args:
            uri: String containing the endpoint to query.
            retries: The number of retries that will be performed if the
                request fails. (Default 3)

        Returns:
            The result of the request in JSON format.

        Throws:
            Exception if retries are exceeded.
        """
        if uri[-5:] != '.json':
            uri = uri + '.json'
        r = Request('GET', uri, headers=self.headers)
        sess = Session()
        rp = sess.prepare_request(r)
        resp = self._retry(lambda: sess.send(rp, verify=False), retries)
        return resp.json()

    def get_latest_entry(self):
        """
        Get the most current reading.

        Returns:
            The latest readings in JSON format.
        """
        return self._get(API_URI_V1 + 'entries/current.json')
