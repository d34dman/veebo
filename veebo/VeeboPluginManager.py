#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from yapsy.PluginManager import PluginManager
from yapsy import log

# ------------------------------------------------------------------------------
# VeeboPluginManager class
# ------------------------------------------------------------------------------


class VeeboPluginManager(PluginManager):

    def activatePluginByName(self, name, category="Default", veebo=None):
        """
        Activate a plugin corresponding to a given category + name.
        """
        pta_item = self.getPluginByName(name, category)
        if pta_item is not None:
            plugin_to_activate = pta_item.plugin_object
            if plugin_to_activate is not None:
                log.debug("Activating plugin: %s.%s" % (category, name))
                plugin_to_activate.activate(veebo)
                return plugin_to_activate
        return None
