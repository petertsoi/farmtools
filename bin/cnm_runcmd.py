#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = """cnm_runcmd -t <timestamp> -u <user> --command="<command>"
\t-t, --timestamp\ttimestamp to put on the sandbox
\t-u, --user\tjob owner
\t--command\tcommand to run
"""
  try:
    opts, args = getopt.getopt(argv,"ht:u:",["timestamp=","user=","command="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  timestamp = None
  user = None
  command = None
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    elif opt in ("-t", "--timestamp"):
      timestamp = arg
    elif opt in ("-u", "--user"):
      user = arg
    elif opt in ("--command"):
      command = arg

  if timestamp and user:
    mybox = Sandbox(timestamp=timestamp, user=user)
  elif timestamp and not user:
    mybox = Sandbox(timestamp=timestamp)
  elif not timestamp and user:
    mybox = Sandbox(user=user)
  else:
    mybox = Sandbox()

  os.chdir(mybox.path)
  if command:
    os.system(command)

if __name__ == "__main__":
  main(sys.argv[1:])

