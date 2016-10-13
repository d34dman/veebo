#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from yapsy.PluginManager import PluginManager
from veebo.Event import *

# ------------------------------------------------------------------------------
# Veebo
# ------------------------------------------------------------------------------


def main():

    dispatcher = EventDispatcher()

    # Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["veebo/plugins"])
    manager.collectPlugins()
    # Loop round the plugins and register events.
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.register_events(dispatcher)


if __name__ == "__main__":
    main()
