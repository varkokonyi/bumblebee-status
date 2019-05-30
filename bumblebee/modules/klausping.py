# pylint: disable=C0111,R0903

"""Displays IP addresses."""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import requests
import re

import subprocess
import os

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        engine.input.register_callback(self,button=bumblebee.input.LEFT_MOUSE, cmd=self.plause)
        self._path=self.parameter("path","")

    def plause(self, _):
        requests.get(self._path+"ping_reset.py")

    def output(self, _):
        self._out=""
        try:
            self._r = requests.get(self._path+'ping_mizu.py')
        except:
            self._out="notget"
            return ""
        if self._r.text.replace("\n","") == "PING":
            _.set("pipi",True)
            return "Ping"
        else:
            _.set("pipi",False)
            return "Clear"
        return self._r.text.replace("\n","")

    def state(self,widget):
        state=[]
        if widget.get("pipi",True):
            return ["critical"]
        else: return []

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
