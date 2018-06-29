# Copyright 2018 Lukas Gangel
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: Documentation and faster method to get list of installed skills

import os

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

__author__ = 'luke5sky'

class WhatCanYouDoSkill(MycroftSkill):

    def __init__(self):
        super(WhatCanYouDoSkill, self).__init__(name="WhatCanYouDoSkill")
        
    @intent_handler(IntentBuilder("").require("What").require("Can").require("Do"))
    def handle_what_can_do__intent(self, message):
        self.speak_dialog("what.i.can")
        myskills = os.popen('msm list | grep installed').read()
        myskills = myskills.replace('\n', ', ').replace('\r', ', ').replace('[installed],', ',').replace('\t', '')
        nr_skills = len(myskills.split())
        nr_skills = 'Here we go, you have %d skills installed.' % nr_skills
        self.speak(nr_skills)
        should_getskills = self.get_response('ask.getskills')
        yes_words = set(self.translate_list('yes'))
        if should_getskills:
            resp_getskills = should_getskills.split()
            if any(word in resp_getskills for word in yes_words):
               self.speak_dialog('my.skills')
               self.speak(myskills.strip())
            else:
               self.speak_dialog('no.skills')


def create_skill():
    return WhatCanYouDoSkill()
