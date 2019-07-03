# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

import math

from tkinter import *
from eg_common import LibC
from fake_redis import newOrCreateConnection


"""
The display module for example
"""
class VaFlower(object):
  def __init__(self, pos, xnum = 36, r0 = 300, r1 = 10, redis_name="0", io_name =("VaFlower", "mic_power")):
    self.redis = newOrCreateConnection(redis_name)
    self.io_name = io_name
    self.redis.subscribe(self.io_name[1], self.io_name[0], self.set_data)

    self.pos = pos
    self.xnum = xnum
    self.r0 = r0
    self.r1 = r1

  def update_view(self):
    self.uisys.gui.after(0, self.update_view0)

  def update_view0(self):
    self.uisys.onTask = True
    sub_ang = math.pi * 2 / self.xnum
    xl = self.r0 * self.ratio
    for xnode in range(self.xnum):
      p0 = self.pos[0] + xl * math.cos(xnode * sub_ang)
      p1 = self.pos[1] + xl * math.sin(xnode * sub_ang)
      bbox = self.uisys.cv.bbox(self.c_list[xnode])
      p0t = (bbox[0] + bbox[2]) / 2
      p1t = (bbox[1] + bbox[3]) / 2
      self.uisys.cv.move(self.c_list[xnode], p0 - p0t, p1 - p1t)

  def set_init(self, uisys):
    self.uisys = uisys
    self.c_list = []
    self.ratio = 1.0
    self.init_over =LibC.rc_cross.event()
    self.uisys.gui.after(0, self.set_init0)
    self.init_over.wait()

  def set_init0(self):
    xd = self.r1 * 2
    for xnode in range(self.xnum):
      self.c_list.append(self.uisys.cv.create_oval(0, 0, xd, xd, fill='pink'))
    self.update_view()
    self.init_over.set()

  def set_data(self, data):
    self.set_ratio(data)

  def set_ratio(self, ratio):
    self.ratio = ratio
    self.update_view()


class VaTk(object):
  ANI_DT = int(1000 / 25)
  def __init__(self, xsize = [800, 800], title = "Example Displayer"):
    self.xsize = xsize
    self.xtitle = title
    self.started = False

  def set_init(self):
    if self.started:
      return
    self.started = True
    self.event_init = LibC.rc_cross.event()
    LibC.rc_line.run(self.set_init0)
    self.event_init.wait()

  def set_end(self):
    if not self.started:
      return
    self.started = False
    self.gui.after(0, self.set_end0)

  def set_init0(self):
    self.gui = Tk()
    self.gui.geometry("{x}x{y}".format(x=self.xsize[0], y=self.xsize[1]))
    self.cv = Canvas(self.gui, width=self.xsize[0], height=self.xsize[1])
    self.cv.pack()
    self.onTask = False
    self.gui.title(self.xtitle)
    self.event_init.set()
    self.update_view()
    self.gui.mainloop()

  def set_end0(self):
    self.gui.destroy()
    self.gui.quit()


  def update_view(self):
    if self.onTask:
      self.onTask = False
      self.gui.update()
    self.gui.after(self.ANI_DT, self.update_view)


