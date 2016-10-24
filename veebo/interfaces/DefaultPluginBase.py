#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin
import logging

class DefaultPluginBase(IPlugin):

    def __init__(self):
        self.veebo = False
        self.is_activated = False

    def run(self):
        return True

    def activate(self, veebo):
        self.is_activated = True
        logging.info('activating..')

    def deactivate(self):
        self.is_activated = False
        logging.info('deactivating..')