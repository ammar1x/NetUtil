
import socket
import os
import argparse
import sys
import datetime
import logging




# logger conf
logging.basicConfig(level = logging.DEBUG,
						format = "%(asctime)s %(levelname)-5s --- %(message)s",
						stream = sys.stdout,
						datefmt = "%d-%m-%Y %H:%M"  )

logger = logging.getLogger("eser")
logger.setLevel(logging.INFO)


def serve_forever(saddr):

	# temperorary fix
	logger = logging

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind(saddr)
	s.listen(5)


	logger.info("socket bound to %s:%d" % (saddr[0], saddr[1]))
	try:
		while 1:
			cs, addr = s.accept()
			logger.info("New connection established (%s:%d)", addr[0], addr[1])
			d = cs.recv(2048)
			d = d.lower().strip()
			if d == "ping":
				cs.send("pong \n")
			elif d == "pong":
				cs.send("ping \n")
			else:
				cs.send("unknown command\n")
			
			cs.close()
			logger.info("Client(%s:%d) was served and disconnected", addr[0], addr[1])

	except IOError as (errno, strerror):
		logger.error("I/O error - %d: %s", errno, strerror)
	except KeyboardInterrupt:
		logger.info("keyboard interrupt. Closing the client")
	except Exception:
		logger.exception("Unkown error")

	try:
		s.close()
		logger.info("server closed successfully")
	except IOError as (errno, strerror):
		logger.error("error while closing the server - (%s:%d)", errno, strerror)




TOOL_DESC = """Start echo server. If no arguments are provided it starts a server with 127.0.0.1:1234 socket address."""


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=TOOL_DESC)
	parser.add_argument("--host", required = False,help="host name of the server", type=int)
	parser.add_argument("--port", required = False, help="port of the server", type=int)
	parser.add_argument("-v", action="store_true", help="be verbose. Default value is true.")
	
	
	args = parser.parse_args()

	if args.v:
		logger.setLevel(logging.INFO)
	else:
		logger.setLevel(logging.WARNING)

	# default configuration
	host, port = ("", 1234)	

	if args.host:
		host = args.host
	if args.port:
		port = args.port
	
	serve_forever((host, port))
		
	
