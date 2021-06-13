import argparse
import sys

from Server.Server import Server

# Create argument parser for command line arguments
parser = argparse.ArgumentParser(description="Options for the swarm server.")
parser.add_argument('--camera', '-c', type = int, default = 0, help = "define the GPS camera index")
parser.add_argument('--noGui', choices=['search', 'calibrate', 'scatter'], help = "run action without starting the GUI")

# Create server instance and start the server
# This file needs te be ran directly and can't be inported
if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    server = Server(args.camera, args.noGui)
    server.start()