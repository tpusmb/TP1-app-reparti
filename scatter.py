#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from mpi4py import MPI
print("zerzer")

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/scatter.log",
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

print("rzerze")
comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()

tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]

chunk_size = int(len(tab) / size) + 1
print("Hi from <" + str(me) + ">")
if me == 0:

    for i in range(size):
        deb = i * chunk_size
        if i == size - 1:
            fin = len(tab) - 1
        else:
            fin = (i + 1) * chunk_size - 1
        comm.send(tab[deb:fin], dest=i, tag=99)
else:
    buf = comm.recv(source=0, tag=99)
    print("I'm <" + str(me) + ">: receive {}".format(buf))

