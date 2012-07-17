# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to stoporse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from QtCore import QDateTime, QObject, QRegExp, Signal

from ..message import Message

class LocationFilter(QObject):
    """
    Contains filter logic for a single location filter. If the regex flag is False
    simple 'is this in that' text matching is used on _text. If the regex flag is True 
    _text is treated as a regular expression with one exception. If it does not
    start with a ^ a .* is appended, and if it does not end with a $ then a .*
    is added to the end.
    The filter_changed signal should be connected to a slot which notifies the
    overall filtering system that it needs to reevaluate all entries.
    """
    filter_changed_signal = Signal()
    def __init__(self):
        super(LocationFilter, self).__init__()
        self._enabled = True

        self._text = ''
        self._regex = False

    def set_text(self, text):
        """
        Setter for _text
        :param text: text to set ''str''
        :emits filter_changed_signal: If _enabled is true
        """
        self._text = text
        if self._enabled:
            self.filter_changed_signal.emit()

    def set_regex(self, checked):
        """
        Setter for _regex
        :param checked" boolean flag to set ''bool''
        :emits filter_changed_signal: If _enabled is true
        """
        self._regex = checked
        if self._enabled:
            self.filter_changed_signal.emit()

    def set_enabled(self, checked):
        """
        Setter for _enabled
        :param checked" boolean flag to set ''bool''
        :emits filter_changed_signal: Always
        """
        self._enabled = checked
        self.filter_changed_signal.emit()

    def is_enabled(self):
        return self._enabled

    def test_message(self, message):
        """
        Tests if the message matches the filter.
        If the regex flag is False simple 'is this in that' text matching is used 
        on _text. If the regex flag is True _text is treated as a regular expression 
        with one exception. If it does not start with a ^ a .* is appended, and if 
        it does not end with a $ then a .* is added to the end.

        :param message: the message to be tested against the filters, ''Message''
        :returns: True if the message matches, ''bool''
        """
        if self._text != '':
            if self._regex:
                temp = self._text
                if temp[0] != '^':
                    temp = '.*' + temp
                if temp[-1] != '$':
                    temp += '.*'
                if QRegExp(temp).exactMatch(message._location):
                    return True
            else:
                if message._location.find(self._text) != -1:
                    return True
        return False
