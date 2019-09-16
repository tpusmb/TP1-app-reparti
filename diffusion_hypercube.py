#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import math
import logging.handlers

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
sender_id = 0
MSG_TO_SEND = ["hello"]
print("Hi from <" + str(me) + ">")


def diffusion(frome, msg):

    if me == frome:
        for dim in range(size):
            next_id = me + pow(2, dim)
            if next_id > size:
                break
            next_id %= size
            print("I'm <{}>: send to {}".format(me, next_id))
            comm.send(msg + [dim], dest=next_id, tag=99)
    else:
        buf = comm.recv(source=sender_id, tag=99)
        for dim in range(int(buf[-1]) + 1, size):
            next_id = me + pow(2, dim)
            if next_id > size:
                break
            next_id %= size
            print("I'm <{}>: send to {}".format(me, next_id))
            comm.send(msg + [dim], dest=next_id, tag=99)

diffusion(0, MSG_TO_SEND)