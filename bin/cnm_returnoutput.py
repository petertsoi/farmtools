#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Cloud import *
from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = "cnm_returnoutput -u <user> -j <job id> -t <task id> -o <output dir>"
  try:
    opts, args = getopt.getopt(argv,"h:u:j:t:o:",["user=","jid=","tid=","output="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  user = None
  jid = None
  tid = None
  outputdir = None
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
    elif opt in ("-o", "--output"):
      outputdir = arg

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

  if outputdir:
    os.chdir(mybox.path)
    fullpath = os.path.join(mybox.path, outputdir)
    if os.path.exists(fullpath):
      Cloud.UploadDir(outputdir)
    else:
      raise Exception("Output directory does not exist: %s" % fullpath)


if __name__ == "__main__":
  main(sys.argv[1:])

