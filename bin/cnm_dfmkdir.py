#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = "cnm_dfmkdir -u <user> -j <job id> -t <task id>"
  try:
    opts, args = getopt.getopt(argv,"h:u:j:t:",["user=","jid=","tid="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  if os.environ.has_key("FARM_DISKFARMROOT"):
    dfroot = os.environ["FARM_DISKFARMROOT"]
  else:
    raise Exception("FARM_DISKFARMROOT not defined")
  user = None
  jid = None
  tid = None
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    elif opt in ("-u", "--user"):
      user = arg
    elif opt in ("-j", "--jid"):
      jid = arg
    elif opt in ("-t", "--tid"):
      tid = arg
  
  if dfroot and user and jid and tid:
    dirpath = os.path.join(dfroot, user, jid, tid)
    if not os.path.exists(dirpath):
      os.umask(0o002)
      os.makedirs(dirpath, 0o775)

if __name__ == "__main__":
  main(sys.argv[1:])

