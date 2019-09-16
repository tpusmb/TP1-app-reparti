#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier pour la diffusion centralisee.

Usage:
    diffusion_centralize.py <id>

Options:
    -h --help           Show this screen.
    <id>                id de celui qui envoie.
"""

from __future__ import absolute_import
import logging.handlers
import os
from mpi4py import MPI
from docopt import docopt

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/diffusion_centralise.log",
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


def diffusion_centralize(node_id):
    comm = MPI.COMM_WORLD
    me = comm.Get_rank()
    size = comm.Get_size()
    print("Hi from <" + str(me) + ">")
    if me == node_id:
        buf = ["coucou"]
        print("I'm <" + str(me) + ">: send " + buf[0])
        for i in range(0, size):
            if i != node_id:
                comm.send(buf, dest=i, tag=99)
    else:
        buf = comm.recv(source=node_id, tag=99)
        print("I'm <" + str(me) + ">: receive " + buf[0])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    diffusion_centralize(int(arguments["<id>"]))
