from json import dump, load
from os import environ, path

class Env:
  _environ = {}
  _cache = None
  def __init__(self, cache=None):
    if cache:
      self._cache = cache
      if path.exists(cache):
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

  def _read_cache(self):
    if self._cache and path.exists(self._cache):
      with open(self._cache, "rb") as f:
        self._environ = load(f)
    else:
      raise Exception("Tried reading from non-existent environment cache")

  def _write_cache(self):
    if self._cache:
      if path.exists(path.dirname(self._cache)):
        with open(self._cache, "wb") as f:
          dump(self._environ, f)
      else:
        raise Exception("Could write to non-existent directory at %s" % self._cache)
