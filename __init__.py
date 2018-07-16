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

import os

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.audio import wait_while_speaking 

__author__ = 'luke5sky'

class WhatCanYouDoSkill(MycroftSkill):

    def __init__(self):
        super(WhatCanYouDoSkill, self).__init__(name="WhatCanYouDoSkill")
        
    @intent_handler(IntentBuilder("").require("What").require("Can").require("Do"))
    def handle_what_can_do__intent(self, message):
        self.speak_dialog("what.i.can") # tell user what he can do
        self.getSkills() # execute function getSkills -> get list of installed skills

    def getSkills(self):
        self.myskills = os.popen('msm list | grep installed').read() # get list of skills via msm and search for "installed"
        self.myskills = self.myskills.replace('\n', ', ').replace('\r', ', ').replace('[installed],', ',').replace('\t', '') # replace unwanted characters and make nice list
        nr_skills = len(self.myskills.split()) # get number of skills
        if nr_skills < 1: # if msm did not give us what we want (no matter why) do alternative skill search
           self.myskills = os.popen('ls /opt/mycroft/skills/').read() # Get folders in /opt/mycroft/skills
           self.myskills = self.myskills.replace('\n', ', ').replace('\r', ', ').replace('\t', '') # replace unwanted characters and make nice list
           nr_skills = len(self.myskills.split()) # get number of skills
        if nr_skills < 1: # if msm and alternative skill search fails than tell user that we couldn't do the job
           wait_while_speaking() # always wait
           self.speak_dialog("not.found") # tell user that we couldn't do the job
           return # if all fails, return
        wait_while_speaking() # always wait
        self.speak_dialog('found', {'nrskills': nr_skills}) # we found skills -> yeah. tell user how many!
        wait_while_speaking() # always wait
        self.should_getskills = self.get_response('ask.getskills') # ask user if we should give him a list of all his skills.
        self.yes_words = set(self.translate_list('yes')) # get list of confirmation words
        self.listSkills() # execute function listSkills -> if user confirmed -> give him a list of all his skills, else -> exit
      
    def listSkills(self):
        if self.should_getskills: # if user said something
           resp_getskills = self.should_getskills.split() # split user sentence into list
           if any(word in resp_getskills for word in self.yes_words): # if any of the words from the user sentences is yes
              self.speak_dialog('my.skills') # Introduction that we will give user list of skills
              self.speak(self.myskills.strip()) # tell user list of skills
           else: # no word in sentence from user was yes
              self.speak_dialog('no.skills') # give user feedback

    def shutdown(self):
        super(WhatCanYouDoSkill, self).shutdown()

    def stop(self):
        pass

def create_skill():
    return WhatCanYouDoSkill()
