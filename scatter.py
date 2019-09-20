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

tab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]


def scatter(from_id, tab, mpi_obj):
    me = mpi_obj.me
    size = mpi_obj.size
    chunk_size = int(len(tab) / size) + 1
    if me == from_id:
        for i in range(size):
            deb = i * chunk_size
            if i == size - 1:
                fin = len(tab) - 1
            else:
                fin = (i + 1) * chunk_size - 1
            if i == from_id:
                print(tab[deb:fin + 1])
            else:
                mpi_obj.comm.send(tab[deb:fin + 1], dest=i, tag=99)
    else:
        buf = mpi_obj.comm.recv(source=MPI.ANY_SOURCE, tag=99)
        print("I'm <" + str(me) + ">: receive {}".format(buf))


if __name__ == "__main__":
    scatter(1, tab, MPIObj())
