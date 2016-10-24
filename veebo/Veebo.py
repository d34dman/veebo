#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
import threading
from state_machine import *

# from yapsy.PluginManager import PluginManager
from veebo.VeeboPluginManager import VeeboPluginManager
from veebo.interfaces.SystemPluginBase import SystemPluginBase
from veebo.interfaces.DefaultPluginBase import DefaultPluginBase
from veebo.EventDispatcher import EventDispatcher
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
        self.logger = logging.getLogger('veebo')
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
            self.path['library'], 'plugins')
        self.path['user_plugins'] = os.path.expanduser(
            os.getenv('VEEBO_CONFIG', '~/.veebo/plugins'))

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
                logging.config.dictConfig(self.config['logging'])

        except OSError:
            self.logger.error("Can't open config file: '%s'",
                          self.path['config_file'])
            raise


    def health_check_config_dir(self):
        # Check if config direcotry present
        if not os.path.exists(self.path['config']):
            try:
                # Try creating the config directory
                os.makedirs(self.path['config'])
            except OSError:
                self.logger.error("Can't create configuration directory: '%s'",
                              self.path['config'])
                raise

        # Check if config directory is writable
        if not os.access(self.path['config'], os.W_OK):
            self.logger.error("Configuration directory '%s' is not writable.",
                          self.path['config'])

    def __del__(self):
        self.plugin_manager = None
        self.event_dispatcher = None
        if not self.is_stopping:
            self.quit()

    def initializePlugins(self):
        plugin_categories = {
            "System": SystemPluginBase,
            "Default": DefaultPluginBase,
        }
        self.plugin_manager = VeeboPluginManager()
        self.plugin_manager.setPluginPlaces(
            [self.path['plugins'], self.path['user_plugins']])

        self.plugin_manager.setCategoriesFilter(plugin_categories)
        # Load the plugins from the plugin directory.
        self.plugin_manager.collectPlugins()
        thread_list = []

        for plugin_category in self.config['plugins']['active']:
            self.plugin_manager.getPluginsOfCategory(plugin_category)
            for plugin_name in self.config['plugins']['active'][plugin_category]:
                plugin = self.plugin_manager.getPluginByName(
                    plugin_name,
                    category=plugin_category)
                if plugin:
                    self.logger.debug("Activating plugin %s in %s", plugin_name, plugin_category)
                    self.plugin_manager.activatePluginByName(
                        plugin.name,
                        category=plugin_category,
                        veebo=self)
                    if "run" in dir(plugin.plugin_object):
                        self.logger.debug("Run method found in plugin %s in %s", plugin_name, plugin_category)
                        t = threading.Thread(target=plugin.plugin_object.run)
                        thread_list.append(t)
                else:
                    self.logger.error("Plugin not found %s in %s", plugin_name, plugin_category)

        for thread in thread_list:
            thread.start()
