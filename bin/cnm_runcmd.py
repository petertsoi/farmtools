#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = """cnm_runcmd -u <owner> -j <job id> -t <task id> -c <command>
  \t-u, --user\tjob owner
  \t-j, --jid\ttractor job id
  \t-t, --tid\ttractor task id
  \t-c, --command\tcommand to run
  """
  try:
    opts, args = getopt.getopt(argv,"h:u:j:t:c:",["user=","jid=","tid=","command="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  user = None
  jid = None
  tid = None
  command = None
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
    elif opt in ("-c", "--command"):
      command = arg

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

  if command:
    os.chdir(mybox.path)
    print "Running %(command)s" % locals()
    os.system(command)

if __name__ == "__main__":
  main(sys.argv[1:])

