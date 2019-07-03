# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

"""
A Fake Redis like class.
Used to share messages between modules
It is NOT thread-safe code
"""
class Fake_Redis(object):
  def __init__(self):
    self.hub = {}

  def subscribe(self, name, id, callback):
    node = self.hub.setdefault(name, {})
    node.setdefault(id, callback)

  def unsubscribe(self, name, id):
    node = self.hub.get(name, {})
    node.pop(id, None)
    if len(node) == 0:
      self.hub.pop(name)

  def publish(self, name, *args):
    node = self.hub.get(name, {})
    for func in node.values():
      func(*args)

  def clear(self):
    self.hub.clear()

REDIS_HUBS = {}

def newOrCreateConnection(name):
  if name in REDIS_HUBS:
    return REDIS_HUBS[name]
  redis = Fake_Redis()
  REDIS_HUBS[name] = redis
  return redis