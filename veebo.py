#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import Queue
import threading

from yapsy.PluginManager import PluginManager
from veebo.Event import *

# ------------------------------------------------------------------------------
# Veebo
# ------------------------------------------------------------------------------


def main():

    dispatcher = EventDispatcher()

    # Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["veebo/plugins", "~/.veebo/plugins"])
    manager.collectPlugins()

    q = Queue.Queue()

    thread_list = []

    for plugin in manager.getAllPlugins():
        plugin.plugin_object.register_events(dispatcher)
        t = threading.Thread(target=plugin.plugin_object.run)
        thread_list.append(t)

    for thread in thread_list:
        thread.start()

    while True:
        try:
            print('.')
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            dispatcher.dispatch_event(
                VeeboEvent( VeeboEvent.STOP, 'veebo_core: Quit' )
            )
            break

    print "Quitting Veebo"

if __name__ == "__main__":
    main()
