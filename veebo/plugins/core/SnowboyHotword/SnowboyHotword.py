#!/usr/bin/env python
# -*- coding: utf-8 -*-

from veebo.interfaces.DefaultPluginBase import DefaultPluginBase
import logging
import sys
import time


class SnowboyHotword(DefaultPluginBase):

    def __init__(self):
        self.veebo = False
        self.is_activated = False

    def activate(self, veebo):
        self.is_activated = True
        self.veebo = veebo
        self.config = self.veebo.config['plugins']['config']['SnowboyHotword']
        # Pick up models
        hotwords = self.config['hotwords']
        models = []
        for hotword in hotwords:
            models.insert(hotword, hotwords[hotword]['model'])

        sensitivity = [0.5]*len(models)

        # Obtain snowboy directory from configuration to load the whole library
        snowboy_dir = self.config['snowboy']['dir']
        sys.path.insert(0, snowboy_dir)
        import snowboydecoder
        self.detector = snowboydecoder.HotwordDetector(
            models, sensitivity=sensitivity)

    def interrupt_check(self):
        return self.veebo.is_stopping

    def snowboy_detected(self, hotword):
        logger = self.veebo.logger
        if self.veebo.is_sleeping:
            logger.debug('Hotword detected while sleeping')
            logger.debug(hotword)
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
            logger.debug("Hotword detected while not sleeping")
            logger.debug(hotword)

    def run(self):
        hotwords = self.config['hotwords']
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
