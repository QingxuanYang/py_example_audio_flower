# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

import pyaudio

from eg_common import LibC
from fake_redis import newOrCreateConnection


"""
The microphone module for example
"""
class VaMic(object):
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  CHUNK = 1024

  def __init__(self, redis_name="0", io_name =("VaMic", "mic_control", "mic_chunk"), SIZE_CHUNK = 1024):
    self.redis = newOrCreateConnection(redis_name)
    self.io_name = io_name
    self.redis.subscribe(self.io_name[0], self.io_name[1], self.mic_control)
    self.size_chunk = SIZE_CHUNK
    self.stream = 0

  def mic_control(self, command):
    if command == "+":
      self.set_start()
    if command == "x":
      self.set_end()

  def rectask(self):
    while True:
      if self.stream == 0:
        break
      data = self.stream.read(self.size_chunk)
      self.redis.publish(self.io_name[2], data)
    self.end_waiter.set()

  def set_start(self):
    if self.stream != 0:
      return
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.size_chunk)
    self.end_waiter = LibC.rc_cross.event()
    LibC.rc_line.run(self.rectask)

  def set_end(self):
    if self.stream == 0:
      return
    st = self.stream
    self.stream = 0
    self.end_waiter.wait()
    st.stop_stream()
    st.close()
    self.audio.terminate()


