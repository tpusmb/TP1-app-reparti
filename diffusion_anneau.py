#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fichier pour la diffusion en anneau.

Usage:
    diffusion_anneau.py <id>

Options:
    -h --help           Show this screen.
    <id>                id de celui qui envoie.
"""

from __future__ import absolute_import
import logging.handlers
import os
from docopt import docopt
from mpi4py import MPI

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/diffusion_anneau.log",
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


def diffusion_anneau_un_sens(node_id, buf):
    comm = MPI.COMM_WORLD
    me = comm.Get_rank()
    size = comm.Get_size()
    print("Hi from <" + str(me) + ">")
    if me == node_id:
        print("I'm <" + str(me) + ">: send " + buf[0])
        comm.send(buf, dest=(node_id + 1) % size, tag=99)
    else:
        buf = comm.recv(source=(me - 1 + size) % size, tag=99)
        print("I'm <" + str(me) + ">: receive " + buf[0])
        if me != (node_id - 1) % size:
            print("I'm <" + str(me) + ">: send " + buf[0])
            comm.send(buf, dest=(me + 1) % size, tag=99)


def diffusion_anneau_double_sens(node_id, buf):
    comm = MPI.COMM_WORLD
    me = comm.Get_rank()
    size = comm.Get_size()
    halfway = int(node_id + size / 2) % size
    print("Hi from <" + str(me) + ">")
    if me == node_id:
        print("I'm <" + str(me) + ">: send " + buf[0])
        comm.send(buf, dest=(me + 1) % size, tag=99)
        comm.send(buf, dest=(me - 1 + size) % size, tag=99)
    else:
        if me >= halfway:
            buf = comm.recv(source=(me - 1 + size) % size, tag=99)
            print("I'm <" + str(me) + ">: receive " + buf[0])
            if me != halfway:
                print("I'm <" + str(me) + ">: send " + buf[0])
                comm.send(buf, dest=(me + 1) % size, tag=99)
        else:
            buf = comm.recv(source=(me + 1 + size) % size, tag=99)
            print("I'm <" + str(me) + ">: receive " + buf[0])
            if me != halfway:
                print("I'm <" + str(me) + ">: send " + buf[0])
                comm.send(buf, dest=(me - 1 + size) % size, tag=99)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    diffusion_anneau_un_sens(int(arguments["<id>"]), ["coucou"])
    # diffusion_anneau_double_sens(int(arguments["<id>"]), ["coucou"])
