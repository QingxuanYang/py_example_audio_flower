# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

import numpy as np

from eg_common import LibC
from fake_redis import newOrCreateConnection


"""
The logic module for example
"""
class VaPowerLogic(object):
  def __init__(self, redis_name="0", io_name =("VaPowerLogic", "mic_chunk", "mic_power")):
    self.redis = newOrCreateConnection(redis_name)
    self.io_name = io_name
    self.redis.subscribe(self.io_name[1], self.io_name[0], self.mic_chunk)
    self.data_block = []

  def mic_chunk(self, data):
    self.data_block.append(data)
    if len(self.data_block) >= 2:
      dt2 = self.data_block
      self.data_block = []
      LibC.rc_pool.run(self.in_data0, dt2)

  def in_data0(self, chunks):
    ck2 = b''.join(chunks)
    ck3 = np.fromstring(ck2, dtype=np.int16)
    ck4 = ck3.astype(np.float32)
    ck5 = ck4 ** 2
    ck6 = np.average(ck5)
    ck7 = ck6 / 1000000000.0
    if ck7 > 1:
      ck7 = 1
    # print(ck7)
    self.redis.publish(self.io_name[2], ck7)
