from os import environ, makedirs, path, remove, rmdir, walk
from time import localtime, strftime

class Sandbox:
  def __init__(self, name=None, user=None):
    if name:
      self.name = name
    else:
      if environ.has_key("FARM_JOBTIMESTAMP"):
        timestamp = environ["FARM_JOBTIMESTAMP"]
      else:
        timestamp = strftime("%Y%m%d%H%M%S", localtime())
      if user:
        self.name = "%(user)s_%(timestamp)s" % locals()
      elif environ.has_key("FARM_JOBOWNER"):
        user = environ["FARM_JOBOWNER"]
        self.name = "%(user)s_%(timestamp)s" % locals()
      else: 
        self.name = "cnm_%(timestamp)s" % locals()

  def create(self, scratchdir=None):
    if scratchdir:
      self._scratchdir = scratchdir
    elif environ.has_key("FARM_SCRATCHDIR"):
      self._scratchdir = environ["FARM_SCRATCHDIR"]
    else:
      raise Exception("Scratch directory not defined!")
    if self._scratchdir[-1] != '/':
      scratchdir = self._scratchdir + '/'
    
    if self._scratchdir[-1] != '/':
      self._scratchdir = self._scratchdir + '/'

    self.path =  "%s%s/" % (self._scratchdir, self.name)
    makedirs(self.path)

  def destroy(self):
    if path.exists(self.path):
      for root, dirs, files in walk(self.path, topdown=False):
        for name in files:
          remove(path.join(root, name))
        for name in dirs:
          rmdir(path.join(root, name))
      rmdir(self.path)
