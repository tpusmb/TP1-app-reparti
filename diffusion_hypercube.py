#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from mpi4py import MPI

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

comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()
nb_node = size - 1
MSG_TO_SEND = ["hello"]
print("Hi from <" + str(me) + ">")

# log2(size) pour avoire le nb de dim


def diffusion(from_id, msg):
    if me == from_id:
        start_dim = 0
    else:
        buf = comm.recv(source=MPI.ANY_SOURCE, tag=99)
        start_dim = int(buf[-1]) + 1
        print("I'm {}: {}".format(me, buf))
    for dim in range(start_dim, size):
        next_id = me + pow(2, dim)
        if next_id - nb_node > 0:
            break
        next_id %= size
        print("I'm <{}>: send to {}".format(me, next_id))
        comm.send(msg + [dim], dest=next_id, tag=99)


diffusion(0, MSG_TO_SEND)
