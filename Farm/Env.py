from json import dump, load
from os import environ, path

class Env:
  _environ = {}
  _cachepath = None
  def __init__(self, cache=None):
    if cache:
      self._cachepath = cache
      if path.exists(self._cachepath):
        self._read_cache()
    self.Sync()

  def Get(self, key):
    if self._environ.has_key(key):
      return str(self._environ[key])
    elif environ.has_key(key):
      self._environ[key] = environ[key]
      return str(self._environ[key])
    else:
      return None

  def Put(self, key, value):
    if value:
      value_str = str(value)
      self._environ[key] = value_str
      environ[key] = value_str
    else:
      del self._environ[key]
      del environ[key]
    self._write_cache()

  def Sync(self):
    cache_keys = self._environ.keys()[:]
    for k,v in environ.items():
      if k in cache_keys:
        cache_keys.remove(k)
      else:
        self._environ[k] = v
    for k in cache_keys:
      environ[k] = self._environ[k]
    self._write_cache()

  def SetCachePath(self, cachepath):
    self._cachepath = cachepath

  def _read_cache(self):
    if self._cachepath and path.exists(self._cachepath):
      with open(self._cachepath, "rb") as f:
        self._environ = load(f)
    else:
      raise Exception("Tried reading from non-existent environment cache")

  def _write_cache(self):
    if self._cachepath:
      if path.exists(path.dirname(self._cachepath)):
        with open(self._cachepath, "wb") as f:
          dump(self._environ, f)
      else:
        raise Exception("Could write to non-existent directory at %s" % self._cachepath)
