#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = "cnm_cleanup -u <user> -j <job id> -t <task id>"
  try:
    opts, args = getopt.getopt(argv,"h:u:j:t:",["use=","jid=","tid="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
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

  if user and jid and tid:
    mybox = Sandbox(owner=user, jid=jid, tid=tid)
  elif user and jid and not tid:
    mybox = Sandbox(owner=user, jid=jid)
  elif user and not jid and tid:
    mybox = Sandbox(owner=user, tid=tid)
  elif not user and jid and tid:
    mybox = Sandbox(jid=jid, tid=tid)
  elif not user and not jid and tid:
    mybox = Sandbox(tid=tid)
  elif not user and jid and not tid:
    mybox = Sandbox(jid=jid)
  elif user and not jid and not tid:
    mybox = Sandbox(owner=user)
  else:
    mybox = Sandbox()
  print("Clean up sandbox %s" % mybox.path)
  mybox.Destroy()

if __name__ == "__main__":
  main(sys.argv[1:])

