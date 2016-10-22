#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin
import sys

class SnowboyWakeup(IPlugin):

    def __init__(self):
        self.veebo = False

    def init(self, veebo):
        self.veebo = veebo
        hotword = self.veebo.config['plugins']['SnowboyHotword']['snowboy']['hotword']
        snowboy_dir = self.veebo.config['plugins']['SnowboyHotword']['snowboy']['dir']
        sys.path.insert(0, snowboy_dir)
        import snowboydecoder
        self.detector = snowboydecoder.HotwordDetector(hotword, sensitivity=0.5)

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
