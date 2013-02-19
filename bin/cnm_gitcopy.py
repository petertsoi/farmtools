#!/usr/bin/env python

import os
import sys
import getopt

from farmtools.FS.Sandbox import *

def main(argv):
  __doc__ = """cnm_gitcopy -u <user> -j <job id> -t <task id> -r <repo address> -c <commit SHA> -p <paths to copy>
\t-u, --user\tjob owner
\t-j, --jid\ttractor job id
\t-t, --tid\ttractor task id
\t-r, --repo\trepository address
\t-c, --commit\tcommit SHA (default HEAD)
\t-p, --paths\tpaths to copy (default ALL)
"""
  try:
    opts, args = getopt.getopt(argv,"h:u:j:t:r:c:p:",["user=","jid=","tid=","repo=","commit=","paths="])
  except getopt.error, msg:
    print __doc__
    sys.exit(2)
  user = None
  jid = None
  tid = None
  repoaddr = None
  commit = "HEAD"
  paths = None
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
    elif opt in ("-r", "--repo"):
      repoaddr = arg
    elif opt in ("-c", "--commit"):
      commit = arg
    elif opt in ("-p", "--paths"):
      paths = arg

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

  if repoaddr:
    os.chdir(mybox.path)
    print("Running git archive --format=tar --remote=%(repoaddr)s %(commit)s %(p    aths)s | tar xf -" % locals())
    os.system("git archive --format=tar --remote=%(repoaddr)s %(commit)s %(paths)s | tar xf -" % locals())


if __name__ == "__main__":
  main(sys.argv[1:])

