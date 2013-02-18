from os import makedirs, path, remove, rmdir, walk
from random import random
from time import localtime, strftime

from farmtools.Farm.Env import *

class Sandbox:
  def __init__(self, name=None, owner=None, jid=None, tid=None):
    self.env = Env()
    if name:
      self.name = name
    else:
      if not jid:
        jid = self.env.Get("FARM_JOBID")
        if not jid:
          jid = strftime("%Y%m%d%H%M%S", localtime())
      if not tid:
        tid = self.env.Get("FARM_TASKID")
        if not tid:
          tid = str(int(random()*1000000))
      if not owner:
        owner = self.env.Get("FARM_JOBOWNER")
        if not owner: 
          owner = "cnm"
      self.env.Put("FARM_JOBID", jid)
      self.env.Put("FARM_TASKID", tid)
      self.env.Put("FARM_JOBOWNER", owner)
      self.name = "%(owner)s_%(jid)s_%(tid)s" % locals()
    self.path = self._GeneratePath()
    sandboxpath = self.path
    envpath = "%(sandboxpath)s.farmenv" % locals()
    if path.exists(envpath):
      self.env = Env(envpath)
    else:
      self.Create()

  def Create(self):
    sandboxpath = self.path
    if not path.exists(sandboxpath):
      makedirs(sandboxpath)
      self.env.SetCachePath("%(sandboxpath)s.farmenv" % locals())
      self.env.Sync()

  def Destroy(self):
    if path.exists(self.path):
      for root, dirs, files in walk(self.path, topdown=False):
        for name in files:
          remove(path.join(root, name))
        for name in dirs:
          rmdir(path.join(root, name))
      rmdir(self.path)

  def _GeneratePath(self):
    sandboxname = self.name
    scratchdir = self.env.Get("FARM_SCRATCHDIR")
    if not scratchdir:
      raise Exception("Scratch directory not defined!")
    if scratchdir[-1] != '/':
      scratchdir = scratchdir + '/'
      self.env.Put("FARM_SCRATCHDIR", scratchdir)
    return "%(scratchdir)s%(sandboxname)s/" % locals()
