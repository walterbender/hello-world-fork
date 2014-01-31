# Copyright 2009 Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""HelloWorld Activity: A case study for developing an activity."""

from gi.repository import Gtk
import logging

from gettext import gettext as _

import tempfile
import os
from sugar3.datastore import datastore

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem

class HelloWorldActivity(activity.Activity):
    """HelloWorldActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        padder = Gtk.Alignment.new(xalign=0.5, yalign=0.5,
                                   xscale=0.5, yscale=0.15)
        padder.set_padding(10, 10, 10, 10)
        self.set_canvas(padder)
        padder.show()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        padder.add(vbox)
        vbox.show()

        data = (
            {'label': "Start TurtleBlocks Activity",
             'callback': self.call_activity},
            {'label': "Start activity that can handle the type 'audio/x-vorbis+ogg'",
             'callback': self.call_with_mime},
            {'label': "Start Write Activity with a text object",
             'callback': self.call_activity_with_object},
            {'label': "Start activity that can handle a text object",
             'callback': self.call_with_object},
        )

        for d in data:
            button = Gtk.Button(_(d['label']))
            button.connect('clicked', d['callback'])
            vbox.pack_start(button, True, True, 0)
            button.show()

    def create_text_object(self):
        journal_entry = datastore.create()
        journal_entry.metadata['title'] = "Hello World"
        journal_entry.metadata['mime_type'] = "text/plain"

        temp_path = os.path.join(activity.get_activity_root(), 'instance')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        fd, dest_path = tempfile.mkstemp(dir=temp_path, text=True)
        textfile = os.fdopen(fd, 'w')
        textfile.write("Hello\nWorld!\n\n" * 10)
        textfile.close()
        journal_entry.file_path = dest_path
        datastore.write(journal_entry)

        return journal_entry

    def call_activity(self, *ignore):
        activity.launch_bundle(bundle_id='org.laptop.TurtleArtActivity')

    def call_with_mime(self, *ignore):
        activity.launch_bundle(mime_type='audio/x-vorbis+ogg')

    def call_activity_with_object(self, *ignore):
        activity.launch_bundle(bundle_id='org.laptop.AbiWordActivity',
                               object_id=self.create_text_object().object_id)

    def call_with_object(self, *ignore):
        activity.launch_bundle(object_id=self.create_text_object().object_id)
