# pylint: disable=C0111,R0903

"""Displays current track in VLC."""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import subprocess
import os

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        self._widgets=[]
        super(Module, self).__init__(engine, config,
            self._widgets
        )
        self._title = ""
        engine.input.register_callback(self,button=bumblebee.input.LEFT_MOUSE, cmd=self.plause)

    def update(self,_):
        if os.popen("qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Metadata").read():
            self._widgets=[bumblebee.output.Widget(full_text=self.output)]
        else:
            self._widgets=[]

    def plause(self, _):
        os.popen("qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")

    def output(self, _):
        self._dbus=os.popen("qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Metadata").read()
        if "does not exist" in self._dbus:
            return "o"
        self._temp=self._dbus.split("\n")
        self._out=""
        self._playing=os.popen("qdbus org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlaybackStatus").read()
        if "Playing" in self._playing:
            self._out+=u" \uf04b "
        if "Paused" in self._playing:
            self._out+=u" \uf04c "
        if "Stopped" in self._playing:
            self._out=u"\uf04d"
        self._artist=""
        self._title=""
        for x in self._temp:
            if "xesam:artist:" in x:
                self._artist=x.split(":")[2]
            if "xesam:title:" in x:
                self._title=x.split(":")[2]
        if self._title == "" and self._artist == "":
            return u"\uf057"
        return u"\uf001 "+self._out+self._artist+" -"+self._title
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
