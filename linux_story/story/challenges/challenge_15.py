#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_16 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMv(TerminalMv):
    challenge_number = 15


class Step1(StepTemplateMv):
    story = [
        _("You get the nagging feeling you're missing something."),
        _("What was that spell that helped you find this place?"),
        _("Use it to have a {{lb:closer look around}}.\n")
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls -a}} {{rb:to look more closely around you.}}")
    ]

    story_dict = {
        "CAT, LS, CD, .note": {
            "path": "~/my-house/my-room/.chest"
        }
    }

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls -a"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        _("What's that! There's {{lb:.tiny-chest}} in the corner of the shelter"),
        _("Have a {{lb:look inside}} the {{lb:.tiny-chest}}.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:ls .tiny-chest}} {{rb:to look inside}}")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls .tiny-chest",
        "ls .tiny-chest/",
        "ls -a .tiny-chest",
        "ls -a .tiny-chest/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        _("You see a scroll of parchment inside, with a stamp on it saying "
          "{{lb:MV}}."),
        _("{{lb:Read}} what it says.")
    ]

    hints = [
        _("{{rb:Use}} {{yb:cat .tiny-chest/MV}} {{rb:to read the MV parchment}}")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat .tiny-chest/MV"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        _("{{wb:Edward:}} {{Bb:\"Hey, that's our}} {{lb:.tiny-chest}}{{Bb:. We "
          "use it to keep our possessions safe. "),
        _("I learnt about how to move objects from that}} {{Bb:MV}} "
          "{{Bb:parchment."),
        _("It's probably of more use to you, please take it with my thanks.}}"),
        _("\nMaybe you should go back to {{lb:my-house}} to look for more "
          "hidden items."),
        _("To quickly go back home, use {{yb:cd ~/my-house/}}\n")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/my-house"
    commands = [
        'cd ~/my-house/',
        'cd ~/my-house'
    ]
    hints = [
        _("{{rb:No shortcuts!  Use}} {{yb:cd ~/my-house}} "
          "{{rb:to get back to your house in one step.}}")
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        _("Let's see if we can find anything hidden around here!"),
        _("Where do you think any hidden things could be?"),
        _("Try {{lb:looking closely}} in {{lb:my-room}} first.")
    ]

    start_dir = '~/my-house'

    hints = [
        _("{{rb:Stuck?  Have a look in}} {{yb:my-room}}{{rb:.}}"),
        _("{{rb:Use}} {{yb:ls -a my-room}} {{rb:to look for hidden files in}} "
          "{{lb:my-room}}{{rb:.}}")
    ]

    last_step = True

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.chest' in output:
            return True

        return False

    def next(self):
        NextStep(self.xp)
