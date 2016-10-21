#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from state_machine import *

from yapsy.PluginManager import PluginManager
from EventDispatcher import EventDispatcher


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
        self.initializePlugins()

    def __del__(self):
        self.plugin_manager = None
        self.event_dispatcher = None
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
