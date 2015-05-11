#!/usr/bin/env python
#
#   <Simple Alarm clock written in PyGTK. 
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
import gtk
import os
import pygtk
pygtk.require('2.0')
# local import
import AlarmThread
import Config


#
#
#
class UserInterface:
    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def abortButtonCallBack(self, widget, data=None):
        # is it ok to call delete_event directly? Not quite sure...
        self.delete_event(self.window_,"delete_event", data)
        return True

    def activateButtonCallBack(self, widget, data=None):
        # get parameters, then activate
        # the alarm and freeze the interface:
        alarm_hour=self.spinnerHour_.get_value_as_int()
        alarm_minute=self.spinnerMinute_.get_value_as_int()
        # disable interface input:
        self.spinnerHour_.set_sensitive(False)
        self.spinnerMinute_.set_sensitive(False)
        self.buttonActivate_.set_sensitive(False)
        print(("Activate this alarm %d : %d" % (alarm_hour, alarm_minute)))
        self.alarm_ = AlarmThread.AlarmThread(0,"new alarme",alarm_hour,alarm_minute)
        # Start this alarm's thread:
        self.alarm_.setDaemon(True)
        self.alarm_.start()
        config = Config.Config()
        config.loadConfig()
        config.saveConfig(config.getPlayerCommand(), config.getMusicPath(), alarm_hour, alarm_minute)
        return True
        
    def delete_event(self, widget, event, data=None):
        # popup to confirm exit.
        if(self.quitConfirmation(self.window_,event) == 1):
            if self.alarm_ != None:
                self.alarm_.stop()
            gtk.main_quit()
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return True

    # Another callback (which is not used actually, quit without confirmation)
    def destroy(self, widget, data=None):
        # Stop alarm if any:
        if self.alarm_ != None:
            self.alarm_.stop()
        gtk.main_quit()

    def __init__(self):
        # Create an empty quit dialog
        self.quitDialog_ = None
        # Create an empty about dialog
        self.aboutDialog_ = None
        # Create an empty settings dialog
        self.settingsDialog_ = None
        # Create an empty list of alarms:
        self.alarm_ = None
        # Create an empty Music directory chooser
        self.musicDirectoryChooserButton_ = None
        # create a new window
        self.window_ = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # Create a widget and put it on our main window;
        self.vbox_ = gtk.VBox(False, 0)
        self.window_.add(self.vbox_)
        self.vbox_.show()

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window_.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler delete_event.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window_.connect("destroy", self.delete_event)

        # Sets the border width of the window.
        self.window_.set_border_width(10)
        self.window_.set_title("Alarm clock")
        # set window size
        self.window_.set_size_request(175, 200)
        # set position on screen
        self.window_.set_position(gtk.WIN_POS_CENTER)


        # create a simple menu
        self.Menu()

        # set toolbar icon
        self.window_.set_icon_from_file("alarme.png")

        # create spin buttons entries for hour and minute with respective labels
        config = Config.Config()
        config.loadConfig()
        label = gtk.Label("Hour :")
        label.show()
        self.vbox_.add(label)
        adj = gtk.Adjustment(config.getHour(), 0.0, 23.0, 1.0, 5.0, 0.0)
        self.spinnerHour_ = gtk.SpinButton(adj, 0, 0)
        self.spinnerHour_.set_wrap(True)
        self.spinnerHour_.set_numeric(True)
        self.spinnerHour_.show()
        self.vbox_.add(self.spinnerHour_)

        label = gtk.Label("Minute :")
        label.show()
        self.vbox_.add(label)
        adj = gtk.Adjustment(config.getMinute(), 0.0, 59.0, 1.0, 5.0, 0.0)
        self.spinnerMinute_ = gtk.SpinButton(adj, 0, 0)
        self.spinnerMinute_.set_wrap(True)
        self.spinnerMinute_.set_numeric(True)
        self.spinnerMinute_.show()
        self.vbox_.add(self.spinnerMinute_)


        # Creates a new button with the label "Abort Alarm & Quit".
        self.buttonAbort_ = gtk.Button("Abort Alarm & Quit")
        # Creates a new button with the label "Activate Alarm".
        self.buttonActivate_ = gtk.Button("Activate this alarm")

        # When the buttonAbort receives the "clicked" signal, it will call the
        # function abortButtonCallBack() passing it None as its argument.
        self.buttonAbort_.connect("clicked", self.abortButtonCallBack, None)

        # When the buttonActivate receives the "clicked" signal, it will call the
        # function abortButtonCallBack() passing it None as its argument.
        self.buttonActivate_.connect("clicked", self.activateButtonCallBack, None)

        # This packs the buttons into the window (a GTK container).
        self.vbox_.add(self.buttonAbort_)
        self.vbox_.add(self.buttonActivate_)

        # The final step is to display this newly created widgets.
        self.buttonAbort_.show()
        self.buttonActivate_.show()

        # and the window
        self.window_.show_all()

    def Menu( self ):
        menu = gtk.MenuBar()
        # File
        filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(filemenu)
        # File -> Settings...
        exit = gtk.MenuItem("Settings...")
        exit.connect("activate", self.SettingsDialog)
        filemenu.append(exit)
        # File -> Exit
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", gtk.main_quit)
        filemenu.append(exit)

        # ?
        helpmenu = gtk.Menu()
        helpm = gtk.MenuItem("?")
        helpm.set_submenu(helpmenu)
        # ? -> About
        about = gtk.MenuItem("About")
        about.connect("activate", self.AboutDialog)
        helpmenu.append(about)

        # Insert File in our menu
        menu.append(filem)
        # Insert ? in our menu
        menu.append(helpm)
        # Insert menu in the container widget
        self.vbox_.add(menu)

    # Defines the quit popup content
    def quitConfirmation( self, window, event ):
        # If dialog does not exists, create it
        if self.quitDialog_ == None:
            # Create dialog
            self.quitDialog_ = gtk.Dialog()
 
            # Set it modal and transient for main window.
            self.quitDialog_.set_modal( True )
            self.quitDialog_.set_transient_for( self.window_ )
 
            # Set title
            self.quitDialog_.set_title( 'Do you want to quit PyGTK alarm clock?' )
 
            # Add buttons.
            self.quitDialog_.add_button( gtk.STOCK_YES, 1 )
            self.quitDialog_.add_button( gtk.STOCK_NO,  2 )
 
            # Using non-null parameter list when creating dialog,
            # the last six calls can be written as:
            # self.quitDialog_ = gtk.Dialog( 'Conformation', self,
            #                                gtk.DIALOG_MODAL,
            #                                ( gtk.STOCK_YES, 1,
            #                                  gtk.STOCK_NO,  2 ) )
     
            # Create label
            label = gtk.Label( 'Current alarm if any, will be discarded.' )
     
            # Pack label, taking API change in account
            if gtk.pygtk_version[1] < 14:
                self.quitDialog_.vbox.pack_start( label )
            else:
                self.quitDialog_.get_content_area().pack_start( label )
     
            # Show dialog
            self.quitDialog_.show_all()
     
        # Run dialog
        response = self.quitDialog_.run()
        self.quitDialog_.hide()
     
        return response == 1

    # Defines the settings popup content
    def SettingsDialog(self, data = None):
        # Value of this globals might be altered here:
        config = Config.Config()
        if self.settingsDialog_ == None:
            # Create dialog
            self.settingsDialog_ = gtk.Dialog()
 
            # Set it modal and transient for main window.
            self.settingsDialog_.set_modal( True )
            self.settingsDialog_.set_transient_for( self.window_ )
 
            # Set title
            self.settingsDialog_.set_title( 'Settings' )
 
            # Add buttons.
            self.settingsDialog_.add_button( gtk.STOCK_APPLY, 1 )
            self.settingsDialog_.add_button( gtk.STOCK_CANCEL,  2 )

            # Create label for setting Music directory
            label = gtk.Label( 'Select the music directory you want to play:' )
     
            # Pack label, taking API change in account
            if gtk.pygtk_version[1] < 14:
                self.settingsDialog_.vbox.pack_start( label )
            else:
                self.settingsDialog_.get_content_area().pack_start( label )

            # Choosing directory button + FilChosser window
            self.musicDirectoryChooserButton_ = gtk.FileChooserButton('Select a Directory')
            self.musicDirectoryChooserButton_.set_current_folder(config.getMusicPath())
            self.musicDirectoryChooserButton_.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

            # Pack file chooser button, taking API change in account
            if gtk.pygtk_version[1] < 14:
                self.settingsDialog_.vbox.pack_start( self.musicDirectoryChooserButton_ )
            else:
                self.settingsDialog_.get_content_area().pack_start( self.musicDirectoryChooserButton_ )

            # Create label for setting player
            label = gtk.Label( 'Set the player (note that a playlist will be given as the last argument of this player):' )
     
            # Pack label, taking API change in account
            if gtk.pygtk_version[1] < 14:
                self.settingsDialog_.vbox.pack_start( label )
            else:
                self.settingsDialog_.get_content_area().pack_start( label )
 
            # Player entry:
            self.entryPlayerCommand_ = gtk.Entry(max=0)
            self.entryPlayerCommand_.set_text(config.getPlayerCommand())
            
            # Pack entry, takin API change into account
            if gtk.pygtk_version[1] < 14:
                self.settingsDialog_.vbox.pack_start( self.entryPlayerCommand_ )
            else:
                self.settingsDialog_.get_content_area().pack_start( self.entryPlayerCommand_ )
     
            # Show dialog
            self.settingsDialog_.show_all()

        # Run dialog
        response = self.settingsDialog_.run()
        self.settingsDialog_.hide()
        # If settings were applied, update settings
        if response == 1:
            music_path = os.path.abspath(self.musicDirectoryChooserButton_.get_current_folder())
            print(music_path)
            player = self.entryPlayerCommand_.get_text()
            print(player)
            # Save config while existing
            config.saveConfig(player, music_path, self.spinnerHour_.get_value_as_int(), self.spinnerMinute_.get_value_as_int())
        return response == 1


    # Defines the About popup content
    def AboutDialog(self, data = None):
        if self.aboutDialog_ == None:
            # Create about dialog
            self.aboutDialog_ = gtk.AboutDialog()
            self.aboutDialog_.set_transient_for( self.window_ )
             
            # Set dialog's properties
            self.aboutDialog_.set_program_name( "Simple Alarm clock written in PyGTK." )
            self.aboutDialog_.set_version( "0.2" )
            self.aboutDialog_.set_copyright( "This program is free software, under GPL licence" )
            self.aboutDialog_.set_website( "http://ru.linkedin.com/in/vincenthervieux" )
            self.aboutDialog_.set_authors([ "Vincent Hervieux <vincent.hervieux@gmail.com>" ] )

            # Show dialog
            self.aboutDialog_.show_all()

        # Run dialog
        self.aboutDialog_.run()
        self.aboutDialog_.hide()

    def main(self):
        # thread support for GTK
        gtk.gdk.threads_init()
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

