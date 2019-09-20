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
HDLR = logging.handlers.TimedRotatingFileHandler("log/diffusion_hypercube.log",
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

MSG_TO_SEND = ["hello"]


def diffusion(from_id, msg, mpi_obj):
    me = mpi_obj.me
    size = mpi_obj.size
    if me == from_id:
        start_dim = 0
    else:
        buf = mpi_obj.comm.recv(source=MPI.ANY_SOURCE, tag=99)
        start_dim = int(buf[-1]) + 1
        print("I'm {}: get {}".format(me, buf))
    for dim in range(start_dim, size):
        next_id = me + pow(2, dim)
        if next_id - mpi_obj.nb_node > 0:
            break
        next_id %= size
        print("I'm <{}>: send to {}".format(me, next_id))
        mpi_obj.comm.send(msg + [dim], dest=next_id, tag=99)


if __name__ == "__main__":
    diffusion(0, MSG_TO_SEND, MPIObj())
