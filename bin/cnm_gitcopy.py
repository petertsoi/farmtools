#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = """cnm_gitcopy -t <timestamp> -u <user> -r <repo address> -c <commit SHA> -p <paths to copy>
\t-t, --timestamp\ttimestamp to put on the sandbox
\t-u, --user\tjob owner
\t-r, --repo\trepository address
\t-c, --commit\tcommit SHA (default HEAD)
\t-p, --paths\tpaths to copy (default ALL)
"""
  try:
    opts, args = getopt.getopt(argv,"ht:u:r:c:p:",["timestamp=","user=","repo=","commit=","paths="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  timestamp = None
  user = None
  repoaddr = None
  commit = "HEAD"
  paths = None
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    elif opt in ("-t", "--timestamp"):
      timestamp = arg
    elif opt in ("-u", "--user"):
      user = arg
    elif opt in ("-r", "--repo"):
      repoaddr = arg
    elif opt in ("-c", "--commit"):
      commit = arg
    elif opt in ("-p", "--paths"):
      paths = arg

  if timestamp and user:
    mybox = Sandbox(timestamp=timestamp, user=user)
  elif timestamp and not user:
    mybox = Sandbox(timestamp=timestamp)
  elif not timestamp and user:
    mybox = Sandbox(user=user)
  else:
    mybox = Sandbox()

  if repoaddr:
    os.chdir(mybox.path)
    #os.system("git archive --format=tar --remote=%(repoaddr)s %(commit)s %(paths)s | tar xf -" % locals())
    print("git archive --format=tar --remote=%(repoaddr)s %(commit)s %(paths)s | tar xf -" % locals())


if __name__ == "__main__":
  main(sys.argv[1:])

