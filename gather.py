#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from mpi4py import MPI

from mpi_obj import MPIObj

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/gather.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


def gather(to_id, tab, mpi_obj):
    me = mpi_obj.me
    size = mpi_obj.size
    if me == to_id:
        big_tab = tab
        for i in range(size):
            if i != me:
                buf = mpi_obj.comm.recv(source=MPI.ANY_SOURCE, tag=99)
                big_tab.extend(buf)
        print("I'm <{}>: receive {}".format(me, big_tab))
        return big_tab
    else:
        print("I'm <{}>: send {}".format(me, tab))
        mpi_obj.comm.send(tab, dest=0, tag=99)
        return []


if __name__ == "__main__":
    mpi_obj = MPIObj()
    gather(0, [mpi_obj.me], mpi_obj)
