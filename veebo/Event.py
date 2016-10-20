#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ------------------------------------------------------------------------------
# EventDispatcher class
# ------------------------------------------------------------------------------

class EventDispatcher(object):

    def __init__(self):
        self._events = dict()

    def __del__(self):
        self._events = None

    def has_listener(self, event_type, listener):
        # Check for event type and for the listener
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def dispatch_event(self, event_type, data=None):
        # Dispatch the event to all the associated listeners
        if event_type in self._events.keys():
            listeners = self._events[event_type]

            for listener in listeners:
                listener(data)

    def add_event_listener(self, event_type, listener):
        # Add listener to the event type
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])

            listeners.append(listener)

            self._events[event_type] = listeners

    def remove_event_listener(self, event_type, listener):
        # Remove the listener from the event type
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type]

            if len(listeners) == 1:
                # Only this listener remains so remove the key
                del self._events[event_type]

            else:
                # Update listeners chain
                listeners.remove(listener)

                self._events[event_type] = listeners
