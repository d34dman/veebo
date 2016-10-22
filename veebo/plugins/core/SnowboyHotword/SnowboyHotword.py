#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin
import logging
import sys
import time


class SnowboyHotword(IPlugin):

    def __init__(self):
        self.veebo = False

    def init(self, veebo):
        self.veebo = veebo

        # Pick up models
        hotwords = self.veebo.config['plugins']['SnowboyHotword']['hotwords']
        models = []
        for hotword in hotwords:
            models.insert(hotword, hotwords[hotword]['model'])

        sensitivity = [0.5]*len(models)

        # Obtain snowboy directory from configuration to load the whole library
        snowboy_dir = self.veebo.config['plugins']['SnowboyHotword']['snowboy']['dir']
        sys.path.insert(0, snowboy_dir)
        import snowboydecoder
        self.detector = snowboydecoder.HotwordDetector(
            models, sensitivity=sensitivity)

    def interrupt_check(self):
        return self.veebo.is_stopping

    def snowboy_detected(self, hotword):
        if self.veebo.is_sleeping:
            event_type = hotword['action']
            data = {
                'event': {
                    'type': event_type,
                    'source': 'SnowboyHotword',
                    'time': time.time(),
                },
                'data': hotword['data']
            }
            self.veebo.event_dispatcher.dispatch_event(event_type, data)
        else:
            print 'veebo is already awake'

    def run(self):
        hotwords = self.veebo.config['plugins']['SnowboyHotword']['hotwords']
        callbacks = []
        for hotword in hotwords:
            def __closure(h):
                return lambda: self.snowboy_detected(h)
            callbacks.insert(hotword, __closure(h=hotwords[hotword]))

        self.detector.start(
            detected_callback=callbacks,
            interrupt_check=self.interrupt_check,
            sleep_time=0.03
        )
