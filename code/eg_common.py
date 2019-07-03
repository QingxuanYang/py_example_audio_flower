# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

import traceback

"""
Example support library
"""
LOG_ERROR = print


"""
Runnable Consumer
Start a new thread to run a function
"""
class XRcLine(object):
  def __init__(self):
    from threading import Thread
    from threading import Event
    self.proClass = Thread
    self.proEvent = Event
    self.xid = 0

  def innerRun(self, xtarget, argv):
    try:
      xtarget(*argv)
    except:
      xexec = traceback.format_exc()
      LOG_ERROR(xexec)

  def run(self, xtarget, *argv):
    xname = "rcline_{}".format(self.xid)
    self.xid += 1
    p0 = self.proClass(target=self.innerRun, args=[xtarget, argv], name=xname)
    p0.start()
    return p0

  def event(self):
    return self.proEvent()

"""
Locker for multi-threads
"""
class XRcCross0(object):
  def __init__(self):
    import multiprocessing
    self.mp = multiprocessing

  def event(self):
    return self.mp.Event()

  def lock(self):
    return self.mp.Lock()

  def queue(self):
    return self.mp.Manager().Queue()

"""
Runnable Consumer
Run a function in threading pool
"""
class XRcPoolMP(object):
  MAX_POOL_SIZE = 10
  def __init__(self):
    from multiprocessing.pool import ThreadPool
    self.pool = ThreadPool(self.MAX_POOL_SIZE)

  def innerRun(self, xtarget, argv):
    try:
      xtarget(*argv)
    except:
      xexec = traceback.format_exc()
      LOG_ERROR(xexec)

  def run(self, xtarget, *argv):
    self.pool.apply_async(self.innerRun, [xtarget, argv])



"""
Common Library for this example
"""
class LibC(object):
  rc_cross = XRcCross0()
  rc_line = XRcLine()
  rc_pool = XRcPoolMP()