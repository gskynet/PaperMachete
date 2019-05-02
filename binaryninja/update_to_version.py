#!/usr/bin/env python
# Copyright (c) 2015-2017 Vector 35 LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sys

from binaryninja.update import UpdateChannel, are_auto_updates_enabled, set_auto_updates_enabled, is_update_installation_pending, install_pending_update
from binaryninja import core_version
import datetime

chandefault = UpdateChannel.list[0].name
channel = None
versions = []


def load_channel(newchannel):
    global channel
    global versions
    if channel is not None and newchannel == channel.name:
        pass
    else:
        try:
            print(("Loading channel %s versions ..." % newchannel))
            channel = UpdateChannel[newchannel]
            versions = channel.versions
        except Exception:
            print(("%s is not a valid channel name. Defaulting to " % chandefault))
            channel = UpdateChannel[chandefault]


def select(version):
    if version.version == core_version():
        print(("Already running %s" % version.version))
    else:
        date = datetime.datetime.fromtimestamp(version.time).strftime('%c')
        print("Version:\t%s" % version.version)
        print("Updated:\t%s (%s -> %s)" % (date, core_version(), version.version))
        print("Notes:\n\n-----\n%s" % version.notes)
        print("Downloading...")
        print(version.update())
        print("Installing...")
        if is_update_installation_pending:
            install_pending_update()
        sys.exit()


def list_channels():
    channel_list = UpdateChannel.list
    for index, item in enumerate(channel_list):
        print("%d)\t%s" % (index + 1, item.name))


def toggle_updates():
    set_auto_updates_enabled(not are_auto_updates_enabled())


def main():
    global channel
    load_channel(chandefault)
    command = "update"
    version = "lastest"
    u_version = 0
    print(("Channel:\t%s" % channel.name))
    print(("Version:\t%s" % core_version()))
    print(("Auto-Update:\t%s" % are_auto_updates_enabled()))
    if len(sys.argv) >= 2:
        command = sys.argv[1]
    if len(sys.argv) >= 3:
        version = sys.argv[2]
    if command == "update":
        for _i, v in enumerate(versions):
            if v.version == version or version == "lastest":
                u_version = v
                break
        select(u_version)
    elif command == "version":
        for index, version in enumerate(versions):
            date = datetime.datetime.fromtimestamp(version.time).strftime('%c')
            print("%d)\t%s (%s)" % (index + 1, version.version, date))
    elif command == "channel":
        list_channels()


if __name__ == "__main__":
    main()
