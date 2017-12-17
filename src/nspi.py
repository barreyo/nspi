# -*- coding: utf-8 -*-
"""Script that fetches the information and outputs to the display."""

import argparse
import logging
import os

from ns_api import NightscoutAPI
from screen_writer import ScreenWriter

logger = logging.getLogger(__name__)


def main():
    """TODO."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_root',
                        help='The root of the server to query.',
                        type=str)
    args = parser.parse_args()

    root = None

    if args.server_root:
        logger.info('Server root supplied, using %s', args.server_root)
        root = args.server_root
    else:
        logger.info('No args supplied using env variable NS_SERVER_ROOT')
        root = os.environ['NS_SERVER_ROOT']

    api = NightscoutAPI(server_root=root)
    res = api.get_latest_entry()

    logger.info('Response from server: %s', res)

    writer = ScreenWriter(21, 26, 5, 6, 13, 19)
    writer.write_to_lcd(res['sgv'], res['direction'])


if __name__ == '__main__':
    main()
