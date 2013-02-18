#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = """cnm_cleanup -t <timestamp> -u <user>
\t-t, --timestamp\tcleanup timestamp
\t-u, --user\tjob owner
"""
  try:
    opts, args = getopt.getopt(argv,"ht:u:",["timestamp=","user="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  timestamp = None
  user = None
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    elif opt in ("-t", "--timestamp"):
      timestamp = arg
    elif opt in ("-u", "--user"):
      user = arg

  if timestamp and user:
    mybox = Sandbox(timestamp=timestamp, user=user)
  elif timestamp and not user:
    mybox = Sandbox(timestamp=timestamp)
  elif not timestamp and user:
    mybox = Sandbox(user=user)
  else:
    mybox = Sandbox()

  mybox.Destroy()

if __name__ == "__main__":
  main(sys.argv[1:])

