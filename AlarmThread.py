#!/usr/bin/env python
#
#   <Simple Alarm clock written in PyGTK. 
#    This program was initially based on this Python script: 
#    http://www.junauza.com/2008/04/simple-python-alarm-clock.html >
#
#    Copyright (C) <2011>  <vincent.hervieux@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# external import
import shlex
import subprocess
import time
from threading import Thread
# local import
import Config
#
# Defines what is an alarm:
#
class Alarm(Thread):
    # default constructor:
    def __init__(self):
        Thread.__init__(self)
        self.name_ = "default"
        self.day_ = 0
        self.hour_ = 0
        self.minute_ = 0
        self.keepRunning_ = False
        self.process_ = None

    # Constructor setting parameters:
    def __init__(self, _name, _day, _hour, _minute):
        Thread.__init__(self)
        self.daemon = True
        self.name_ = _name
        self.day_ = _day
        self.hour_ = _hour
        self.minute_ = _minute
        self.keepRunning_ = False
        self.process_ = None

    def play(self):
        config = Config.Config()
    	commandLine = config.getFullCommand();
    	args = shlex.split(commandLine)
        # Lauch process and keep it into context
    	self.process_ = subprocess.Popen(args)

    # Execute the alarm
    def run(self):
        # First set flag that we are running:
        self.keepRunning_ = True
        while(self.keepRunning_):
            # Get current time/date
            dt = list(time.localtime())
            # From it retrieve hour and minute:
            hour = dt[3]
            minute = dt[4]
            # Check if it's time to wake up:
            print "%d %d %d %d" % (hour,minute,self.hour_,self.minute_)
            if (hour == self.hour_) and (minute == self.minute_):
                self.play()
                return
    	    else:
	        	# Relax CPU, we are not in a hurry to wake up ;)
                time.sleep(1)

    def stop(self):
        if self.keepRunning_ :
            # term PID if process is running
            if self.process_ != None:
                self.process_.terminate()
            self.keepRunning_ = False
            self.join()
        # TODO:
        # - mutex to protect this


