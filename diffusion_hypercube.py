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


def sender(msg, ids):
    """

    :param msg:
    :param ids:
    :return:
    """
    for id in ids:
        comm.send(msg, dest=id, tag=99)


def get_next_ids(id):
    ids = []
    for dim in [0, 1, 2]:
        next_id = id * math.pow(2, dim)
        if next_id < size:
            ids.append(next_id)

    return ids


def diffusion_hypercube(id):
    """

    :param id:
    :return:
    """
    if me == 0:
        print("I'm <{}>: send {}".format(me, MSG_TO_SEND))
        sender(MSG_TO_SEND, get_next_ids(me))
    else:
        buf = comm.recv(source=sender_id, tag=99)
        print("I'm <{}>: receive {}".format(me, buf[0]))
        ids = get_next_ids(me)
        if len(ids) == 0:
            print("I'm <{}>: no more send".format(me, buf[0]))
        else:
            sender(MSG_TO_SEND, ids)


