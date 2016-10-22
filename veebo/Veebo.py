#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from state_machine import *

from yapsy.PluginManager import PluginManager
from EventDispatcher import EventDispatcher
import os
import yaml

# ------------------------------------------------------------------------------
# Veebo
# ------------------------------------------------------------------------------

@acts_as_state_machine
class Veebo():

    RESPOND = "Veebo:RESPOND"

    name = 'Veebo'

    initializing = State(initial=True)
    sleeping = State()
    listening = State()
    processing = State()
    stopping = State()

    start = Event(from_states=(initializing),
                  to_state=sleeping)

    listen = Event(from_states=(sleeping, processing),
                   to_state=listening)

    process = Event(from_states=(sleeping, listening),
                    to_state=processing)

    sleep = Event(from_states=(listening, processing),
                  to_state=sleeping)

    quit = Event(from_states=(initializing, sleeping, listening, processing),
                 to_state=stopping)



    def __init__(self):
        self.event_dispatcher = EventDispatcher()
        self.path = {}
        self.path['app'] = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                ),
                os.pardir
            )
        )

        self.path['resources'] = os.path.join(self.path['app'], 'resources')
        self.path['library'] = os.path.join(self.path['app'], 'veebo')
        self.path['plugins'] = os.path.join(
            self.path['library'], 'veebo/plugins')

        self.path['config'] = os.path.expanduser(
            os.getenv('VEEBO_CONFIG', '~/.veebo'))

        self.path['config_file'] = os.path.join(
            self.path['config'], 'profile.yml')

        self.health_check_config_dir()
        self.read_config_file()
        self.initializePlugins()

    def read_config_file(self):

        try:
            with open(self.path['config_file'], "r") as f:
                self.config = yaml.safe_load(f)

        except OSError:
            print("Can't open config file: '%s'", self.path['config_file'])
            raise

    def health_check_config_dir(self):
        # Check if config direcotry present
        if not os.path.exists(self.path['config']):
            try:
                # Try creating the config directory
                os.makedirs(self.path['config'])
            except OSError:
                print("Can't create configuration directory: '%s'",
                      self.path['config'])
                raise

        # Check if config directory is writable
        if not os.access(self.path['config'], os.W_OK):
            print("Configuration directory '%s' is not writable.",
                  self.path['config'])

    def __del__(self):
        self.plugin_manager = None
        self.event_dispatcher = None
        if not self.is_stopping:
            self.quit()

    def initializePlugins(self):
        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces(
            ["veebo/plugins", "~/.veebo/plugins"])
        # Load the plugins from the plugin directory.
        self.plugin_manager.collectPlugins()
        thread_list = []
        for plugin in self.plugin_manager.getAllPlugins():
            plugin.plugin_object.init(self)
            t = threading.Thread(target=plugin.plugin_object.run)
            thread_list.append(t)

        for thread in thread_list:
            thread.start()
