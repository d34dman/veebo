#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import threading
from state_machine import *

from yapsy.PluginManager import PluginManager
from veebo.Event import EventDispatcher

# ------------------------------------------------------------------------------
# Veebo
# ------------------------------------------------------------------------------


@acts_as_state_machine
class Veebo():

    RESPOND = "Veebo:RESPOND"

    name = 'Veebo'

    starting = State(initial=True)
    sleeping = State()
    listening = State()
    processing = State()
    saying = State()
    stopping = State()

    start = Event(from_states=(starting),
                  to_state=sleeping)

    listen = Event(from_states=(sleeping, processing, saying),
                   to_state=listening)

    process = Event(from_states=(sleeping, listening),
                    to_state=processing)

    say = Event(from_states=(sleeping, listening, processing),
                to_state=saying)

    sleep = Event(from_states=(listening, processing, saying),
                  to_state=sleeping)

    quit = Event(from_states=(starting, sleeping, listening,
                              processing, saying),
                 to_state=stopping)

    event_dispatcher = EventDispatcher()

    def __init__(self):
        self.initializePlugins()

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


def main():
    veebo = Veebo()
    veebo.start()
    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            veebo.quit()
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            veebo.quit()
            break

    print "Quitting Veebo"

if __name__ == "__main__":
    main()
