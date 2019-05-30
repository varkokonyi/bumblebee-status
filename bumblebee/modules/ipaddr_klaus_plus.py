# pylint: disable=C0111,R0903

"""Displays IP addresses.

Parameters:
	* ipaddr.ifaces

"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import os
import re

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        self._widgets=[]
        self._outStrs=[]
        self._u=0
        super(Module, self).__init__(engine, config,
            self._widgets
        )
#        self._types=["eth","wifi"]
#        self._ifaces=["eno1","wlp3s0"]
        self._types=self.parameter("types").split(",")
        self._ifaces=self.parameter("list").split(",")
        engine.input.register_callback(self,button=bumblebee.input.LEFT_MOUSE, cmd=self.toggle)
        for x in range (0,len(self._types)):
            self._outStrs.append(str(x))
        for x in range (0,len(self._types)):
            self._widgets.append(bumblebee.output.Widget(full_text=self.getext))
            self._widgets[x].set("ajdi",x)
            self._widgets[x].set("iface",self._ifaces[x])
            self._widgets[x].set("type",self._types[x])

    def toggle(self,_):
        if "enabled" in os.popen("nmcli radio wifi").read():
            os.popen("nmcli radio wifi off")
        else:
            os.popen("nmcli radio wifi on")

    def getext(self,_):
        #print "gete"+str(_)+str(type(_))
        #print _.get("ajdi",-1)
        res=str(os.popen("ip -br addr show "+_.get("iface"," ")).read().split()[1:3])
        if "UP" in res:
            res=res.replace("'UP'",u"\uf00c ")
            res=re.sub('[\[\]\,\']','',res)		#remove junk chars
        else:
            res=" "+u"\uf00d"
        if _.get("type"," ")=="wifi":
            res=u"\uf1eb "+res
            if "enabled" in os.popen("nmcli radio wifi").read():
                res=u"\uf205 "+res
            else:
                res=u"\uf204 "+res
        else:
            res=u"\uf0e8 "+res
        return res

    def update_ol(self,_):
        #print "upd"
        #return "a"
        for x in range(0,len(self._types)):
            res=str(os.popen("ip -br addr show "+self._ifaces[x]).read().split()[1:3])
            if "UP" in res:
                res=res.replace("'UP'",u"\uf00c")
            else:
                res=" "+u"\uf00d"
            if self._types[x]=="wifi":
                res=u"\uf1eb"+res
            else:
                res=u"\uf0e8"+res
            self._outStrs[x]=res
#            try:
#                self._widgets[x].set("full_text",self._outStrs[x])
#            except:
#                pass
                #print "xd"
#_[x].set(full_text,res)
            #self._widgets[x].set(full_text,self._outStrs[x])
        #return self._outStrs

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
