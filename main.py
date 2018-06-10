#!/usr/bin/env python3

import os
import sys
import logging

import superman

logging.basicConfig(level=logging.DEBUG)

_l = logging.getLogger('main')


def run():
    _l.debug(sys.argv)
    pwd = os.path.dirname(os.path.realpath(__file__))
    data_dir = pwd + '/_data/'
    _l.debug(data_dir)

    conf = {
        'argv': sys.argv[1:],
        'data_dir': data_dir,
    }

    pipeline = superman.Pipeline(conf=conf, data_dir=data_dir, force=True)
    pipeline.append_task(superman.PrepareManFiles)

    pipeline.execute()


if __name__ == '__main__':
    run()
