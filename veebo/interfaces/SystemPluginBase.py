#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin
import logging

class SystemPluginBase(IPlugin):

    def __init__(self):
        self.veebo = False
        self.is_activated = False

    def activate(self, veebo):
        self.veebo = veebo
        logging.info('activating..')

    def deactivate(self):
        self.veebo = None
        logging.info('deactivating..')
