#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin
from snowboy import snowboydecoder

class SnowboyWakeup(IPlugin):

    def __init__(self):
        self.veebo = False

    def init(self, veebo):
        self.veebo = veebo
        model = 'veebo.pmdl'
        self.detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

    def interrupt_check(self):
        return self.veebo.is_stopping

    def snowboy_detected(self):
        if self.veebo.is_sleeping:
            print 'waking up veebo'
            self.veebo.listen()
        else:
            print 'veebo is already awake'

    def run(self):
        print 'run...'
        self.detector.start(
            detected_callback=self.snowboy_detected,
            interrupt_check=self.interrupt_check,
            sleep_time=0.03
        )
