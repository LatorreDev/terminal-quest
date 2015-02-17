#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.file_data import HIDDEN_DIR, copy_data
from linux_story.challenges.challenge_15.steps import Step1 as NextStep


class StepTemplateMv(Step):
    challenge_number = 14

    def __init__(self):
        Step.__init__(self, TerminalMv)


class Step1(StepTemplateMv):
    story = [
        "{{wb:Edward:}} \"Hey, since you don't seem to be affected by going"
        " outside, can you gather some food for us?\"",
        "\"We didn't have time to grab any before we went into hiding. "
        "Do you remember seeing any food in your travels?\"\n",
        "...ah!  You have all that food in your {{yb:kitchen}}!",
        "We could give that to this family.",
        "Start by moving the basket to your house."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv basket ../../my-house/kitchen",
        "mv basket ../../my-house/kitchen/",
        "mv basket ~/my-house/kitchen",
        "mv basket ~/my-house/kitchen/",
    ]
    hints = [
        "{{r:Use the command}} {{yb:mv basket ~/my-house/kitchen}} "
        "{{rn:to move the basket to your kitchen}}"
    ]
    basket_file = os.path.join(HIDDEN_DIR, 'my-house/kitchen/basket')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def check_output(self, line):
        return os.path.exists(self.basket_file)

    def next(self):
        Step2()


# Go back to your kitchen
class Step2(StepTemplateMv):
    story = [
        "Now head back to your kitchen."
    ]
    start_dir = ".hidden-shelter"
    end_dir = "kitchen"
    command = [
        "cd",
        "cd ..",
        "cd ../"
        "cd my-house",
        "cd my-house/",
        "cd kitchen",
        "cd kitchen/",
        "cd ../../my-house/kitchen",
        "cd ../../my-house/kitchen/",
        "cd ~/my-house/kitchen",
        "cd ~/my-house/kitchen/",
        "cd my-house/kitchen",
        "cd my-house/kitchen/",
        "cd ../..",
        "cd ../../"
    ]
    hints = [
        "{{r:Use the}} {{yb:cd}} {{rn:command to go back to your kitchen.}}"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def show_hint(self, line, current_dir):

        # decide command needed to get to next part of town
        if current_dir == 'town' or current_dir == '.hidden-shelter':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd':
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise, give them a hint
            else:
                hint = (
                    '{{r:Use}} {{yb:cd ..}} {{rn:to make your way to your}} '
                    '{{yb:kitchen}}'
                )

        elif current_dir == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise give them a hint
            else:
                hint = (
                    '{{r:Use}} {{yb:cd my-house/kitchen}} {{rn:to go into '
                    'your house}}'
                )

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Have a look to remind yourself of the food we have"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{r:Use}} {{yb:ls}} {{rn:To have a look around the kitchen}}"
    ]

    def next(self):
        Step4()


# Move three pices of food into the basket
class Step4(StepTemplateMv):
    story = [
        "Move three pieces of food into your basket",
        "You can move multiple items using {{yb:mv <item1> <item2> basket/}}"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    passable_items = [
        'banana',
        'cake',
        'crossaint',
        'pie',
        'grapes',
        'milk',
        'sandwich'
    ]

    def block_command(self, line):
        line = line.strip()
        separate_words = line.split(' ')

        if "cd" in line:
            return True

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    return True

            return False

    def check_command(self, line, current_dir):
        line = line.strip()
        separate_words = line.split(' ')
        all_items = []

        if separate_words[0] == 'mv' and (separate_words[-1] == 'basket' or
                                          separate_words[-1] == 'basket/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    hint = (
                        '{{rb:You\'re trying to move something that isn\'t in'
                        ' the folder.\n Try using}} {{yb:mv %s basket/}}'
                        % self.passable_items[0]
                    )
                    self.send_hint(hint)
                    return

                else:
                    all_items.append(item)

            for item in all_items:
                self.passable_items.remove(item)

            hint = '{{gb:Well done!  Keep going.}}'

        else:
            hint = '{{rb:Try using}} {{yb:mv %s basket/}}' \
                % self.passable_items[0]

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, line):
        basket_dir = os.path.join(HIDDEN_DIR, 'my-house/kitchen/basket')
        food_files = [
            f for f in os.listdir(basket_dir)
            if os.path.isfile(os.path.join(basket_dir, f))
        ]

        if len(food_files) > 4:
            return True
        else:
            return False

    def next(self):
        Step5()


class Step5(StepTemplateMv):
    story = [
        "Now move the basket to the {{yb:.hidden-shelter}}",

    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = [
        "mv basket ../../town/.hidden-shelter",
        "mv basket ../../town/.hidden-shelter/",
        "mv basket ~/town/.hidden-shelter",
        "mv basket ~/town/.hidden-shelter/",
    ]
    hints = [
        "{{r:Use the command}} {{yb:mv basket ~/town/.hidden-shelter}} "
        "to move the basket to the hidden-shelter"
    ]
    basket_file = os.path.join(HIDDEN_DIR, 'town', '.hidden-shelter', 'basket')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    # This doesn't currently do anything
    def check_output(self, line):
        return os.path.exists(self.basket_file)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        "Finally, go back to the {{yb:.hidden-shelter}} using {{yb:cd}}"
    ]
    start_dir = "kitchen"
    end_dir = ".hidden-shelter"
    command = [
        "cd ../../town/.hidden-shelter/",
        "cd ../../town/.hidden-shelter",
        "cd ~/town/.hidden-shelter/",
        "cd ~/town/.hidden-shelter"
    ]
    hints = [
        "{{r:Use the command}} {{yb:cd ~/town/.hidden-shelter}} "
        "{{r:to get back to the hidden-shelter}}"
    ]

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            return True

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        "{{wn:Talk to the people using}} {{yb:cat}} {{wn:and see how they "
        "react to the food}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    hints = [
        "Talk to everyone using {{yb:cat}}"
    ]
    allowed_commands = {
        "cat Edith": [
            "\n{{wb:Edith:}} You saved my little girl and my dog, and now "
            "you've saved us from starvation...how can I thank you?\n",
            "\n{{wb:Edith:}} You saved my little girl, and now you've saved "
            "us from starvation...how can I thank you?\n",
            "\n{{wb:Edith:}} Sniff...thank you.  I appreciate your kindness. "
            "I can't eat though, I miss my daughter too much...\n",
        ],
        "cat Eleanor": [
            "\n{{wb:Eleanor:}} Yummy! See, I told you doggy, someone would "
            "help us.\n",
            "\n{{wb:Eleanor:}} Oooh, food!  If only doggy was here...\n",
            ""
        ],
        "cat Edward": [
            "\n{{wb:Edward:}} Thank you!  I knew you would come through for "
            "us.\n",
            "\n{{wb:Edward:}} Thank you!  I knew you would come through for "
            "us.\n",
            "\n{{wb:Edward:}} Thank you!  I knew you would come through for "
            "us.\n"
        ],
        "cat dog": [
            "\n{{wb:dog:}} \"Woof!\". \nThe dog seems very excited.\n",
            "",
            ""
        ]
    }
    last_step = True

    def __init__(self):
        # Decide which index to take for each option
        girl = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')
        dog = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/dog')
        self.index = 0

        if not os.path.exists(dog):
            del self.allowed_commands['cat dog']

            if not os.path.exists(girl):
                del self.allowed_commands['cat Eleanor']
                self.index = 2
            else:
                self.index = 1

        StepTemplateMv.__init__(self)

    def check_command(self, line, current_dir):
        if line.strip() in self.allowed_commands.keys():

            hint = self.allowed_commands[line][self.index]
            del self.allowed_commands[line]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                self.send_hint(hint)
                return True

            # If the hint is not empty
            elif hint:
                hint += (
                    "\n{{gb:Talk to}} {{yb:" + str(num_people) +
                    "}} {{gb:other}}"
                )
                if num_people > 1:
                    hint += "{{gb:s}}"
        else:
            hint = (
                "{{rn:Use}} {{yb:" + self.allowed_commands.keys()[0] +
                "}} {{rn:to progress}}"
            )

        self.send_hint(hint)

    def next(self):
        copy_data(15, 1)
        NextStep()
