from os import makedirs, path, remove, rmdir, walk
from time import localtime, strftime

from farmtools.Farm.Env import *

class Sandbox:
  def __init__(self, name=None, user=None):
    self.env = Env()
    if name:
      self.name = name
    else:
      timestamp = self.env.Get("FARM_JOBTIMESTAMP")
      if not timestamp:
        timestamp = strftime("%Y%m%d%H%M%S", localtime())
      if not user:
        user = self.env.Get("FARM_JOBOWNER")
        if not user: 
          user = "cnm"
      self.name = "%(user)s_%(timestamp)s" % locals()
    self.path = self._GeneratePath()
    sandboxpath = self.path
    envpath = "%(sandboxpath)s.farmenv" % locals()
    if path.exists(envpath):
      self.env = Env(envpath)

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
