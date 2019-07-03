# -*- coding: utf-8 -*-
__author__ = 'qingxuan'

import time
from eg_mic import VaMic
from eg_logic import VaPowerLogic
from eg_shower import VaTk, VaFlower
from fake_redis import newOrCreateConnection

"""
A example which can listen sound from microphone and show the amplitude on screen
"""
def main(*argv):
  # start Recording
  mic = VaMic()
  log = VaPowerLogic()
  flower = VaFlower([400, 400])
  gui = VaTk([800, 800])

  gui.set_init()
  flower.set_init(gui)
  mic.mic_control("+")
  time.sleep(100)
  mic.mic_control("x")
  newOrCreateConnection("0").clear()
  gui.in_end()

if __name__ == '__main__':
  main()
