from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler


class WhatCanYouDo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('do.you.can.what.intent')
    def handle_do_you_can_what(self, message):
        self.speak_dialog('do.you.can.what')


def create_skill():
    return WhatCanYouDo()

