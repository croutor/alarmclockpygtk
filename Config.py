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
# external import
import ConfigParser
import os

class Config:
    # default constructor, setting some default values:
    def __init__(self):
        # constant
        self.settingsPath_ = os.path.expanduser("~/.alarmclockpygtk")
        self.configFilename_ = "settings.ini"
        self.playlistFilename_ = "/playlist"
        # ConfigParser instance
        self.config_ = ConfigParser.ConfigParser()
        # Default values that might be overwritten
        self.musicPath_ = os.path.expanduser("~/Music/")
        self.player_ = "mplayer -shuffle -playlist"
        self.hour_ = 7
        self.minute_ = 0

    # Create playlist file
    def createPlaylist(self):
        # create directory if not existing already
        if not os.path.exists(self.settingsPath_):
            os.mkdir(self.settingsPath_, 0755)
        # Read config file if any:
        self.loadConfig()
        # create playlist:
        commandLine = "find \"" + self.musicPath_ + "\" -iname *.mp3 -o -iname *.ogg > " + self.settingsPath_ + self.playlistFilename_;
        #print commandLine 
        #args = shlex.split(commandLine)
        #print args
        #p = subprocess.Popen(args)
        os.system(commandLine)
        print commandLine
        return

    # Load config
    def loadConfig(self):
        self.config_.read(self.settingsPath_ + "/" + self.configFilename_)
        # retrieve Music path from config file, if nothing, set default
        if self.config_.has_option("Music", "dir") :
            self.musicPath_ = self.config_.get("Music", "dir")
        # retrieve player command from config file
        if self.config_.has_option("Player", "bin"):
            self.player_ = self.config_.get("Player", "bin")
        # retrieve old set hour command from config file
        if self.config_.has_option("Alarm", "hour"):
            self.hour_ = self.config_.get("Alarm", "hour")
        # retrieve old set minute command from config file
        if self.config_.has_option("Alarm", "minute"):
            self.minute_ = self.config_.get("Alarm", "minute")


    # SaveConfig
    def saveConfig(self,_playerCommand, _musicPath, _hour, _minute):
        # first update context:
        self.player_ = _playerCommand
        self.musicPath_ = _musicPath
        self.hour_ = _hour
        self.minute_ = _minute
        # then store it to file:
        if not self.config_.has_section("Player"):
            self.config_.add_section("Player")
        self.config_.set("Player", "bin", self.player_)
        if not self.config_.has_section("Music"):
            self.config_.add_section("Music")
        self.config_.set("Music", "dir", self.musicPath_)
        if not self.config_.has_section("Alarm"):
            self.config_.add_section("Alarm")
        self.config_.set("Alarm", "hour", self.hour_)
        self.config_.set("Alarm", "minute", self.minute_)
        with open(self.settingsPath_ + "/" + self.configFilename_, 'wb') as configfileFd: self.config_.write(configfileFd)

    def getPlayerCommand(self):
        command = self.player_
        return command

    def getMusicPath(self):
        self.loadConfig()
        return self.musicPath_

    def getHour(self):
        return float(self.hour_)

    def getMinute(self):
        return float(self.minute_)

    def getFullCommand(self):
        self.createPlaylist()
        return self.player_ + " " + self.settingsPath_ + self.playlistFilename_
         

