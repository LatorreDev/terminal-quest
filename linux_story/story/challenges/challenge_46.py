#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.Animation import Animation
from linux_story.StepTemplate import StepTemplate
from linux_story.common import get_story_file, get_username
from linux_story.helper_functions import wrap_in_box
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_sudo import TerminalSudo
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class StepTemplateSudo(StepTemplate):
    TerminalClass = TerminalSudo


class Step1(StepTemplateRm):
    story = [
        _("{{gb:You saved all the villagers.}}"),
        _("You are alone with the Rabbit and the bell."),
        "",
        _("Time to end this.")
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]
    hints = [
        _("{{rb:Use}} {{yb:rm bell}} {{rb:to remove the bell.}}")
    ]
    dark_theme = True


    def block_command(self, line):
        if line == "rm Rabbit":
            print _("The rabbit dodged the attack!")
            return True
        return StepTemplateRm.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "rm Rabbit":
            self.send_hint(
                _("{{lb:The rabbit dodged the attack!}} {{rb:Remove the bell with}} {{yb:rm bell}}")
            )
            return

        return StepTemplateRm.check_command(self, line)

    def next(self):
        Animation("gong-being-removed").play_finite(1)
        self.send_normal_theme()
        Animation("rabbit-blinking").play_finite(1)
        return 46, 2


class Step2(StepTemplateRm):
    story = [
        _("The anger behind the rabbit's eyes fades, and is replaced with confusion."),
        "",
        _("The Swordmaster runs into the room."),
        "",
        _("Swordmaster: {{Bb:\"You did it! The rabbit is free of the cursed bell, and you've saved everyone who was "
          "kidnapped.\"}}"),
        "",
        _("{{Bb:\"The chest the Rabbit stole is right here. Have you gone through the contents?\"}}"),
        "",
        _("{{lb:Examine the contents of the chest.}}")
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "cat chest/scroll"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat chest/scroll}} {{rb:to examine the contents.}}")
    ]
    deleted_items = [
        "~/woods/thicket/rabbithole/Rabbit"
    ]

    file_list = [
        {
            "path": "~/woods/thicket/rabbithole/Swordmaster",
            "contents": get_story_file("swordmaster-without-sword")
        },
        {
            "path": "~/woods/thicket/rabbithole/Rabbit",
            "contents": get_story_file("Rabbit-cute")
        }
    ]

    def check_command(self, line):
        if line == "cat chest/torn-note":
            return False
        return StepTemplateRm.check_command(self, line)

    def next(self):
        return 46, 3


class Step3(StepTemplateSudo):
    story = wrap_in_box([
        _("{{gb:New Spell:}} Use {{yb:sudo}} to"),
        _(" {{lb:make yourself into a Super User.}}")
    ])
    story += [
        _("Try it out. Use {{yb:sudo ls}} to look around."),
        _("You will be prompted for a password."),
        "",
        _("Swordmaster: {{Bb:The Rabbit couldn't guess the password.}}"),
        _("{{Bb:Can you figure it out?}}"),
        ""
    ]
    commands = [
        "sudo ls",
        "sudo ls .",
        "sudo ls ./"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Try again! Use}} {{yb:sudo ls}} {{rb:and guess a password.}}"
    ]

    def next(self):
        return 46, 4


class Step4(StepTemplateSudo):
    story = [
        "Swordmaster: {{Bb:\"You may not notice a difference, but you became a Super User for a instant.}}",
        "{{Bb:Knowing this command allows you to do things when all else fails.\"}}",
        "",
        "{{gb:Congratulations, you learnt sudo!}}",
        "",
        "{{Bb:\"You should}} {{lb:remove}} {{Bb:this chest so it cannot fall into enemy hands again.}}",
        "{{Bb:To delete the whole chest, use}} {{yb:rm -r chest/}}{{Bb:. The -r flag is used for directories.\"}}"
    ]
    commands = [
        "rm -r chest",
        "rm -r chest/"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [
        "{{rb:Use}} {{yb:rm -r chest}} {{rb:to remove the chest and its contents.}}"
    ]

    def next(self):
        return 46, 5


class Step5(StepTemplateSudo):
    story = [
        "Swordmaster: {{Bb:\"Well done.\"}}",
        "{{Bb:\"Let's go back to town. We should say hi to everyone.\"}}"
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/town"
    file_list = [
        {
            "path": "~/town/Ruth",
            "contents": get_story_file("Ruth")
        },
        {
            "path": "~/town/Clara",
            "contents": get_story_file("Clara")
        },
        {
            "path": "~/town/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]

    def block_command(self, last_user_input):
        return unblock_cd_commands(last_user_input)

    def next(self):
        return 46, 6


class Step6(StepTemplateSudo):
    story = [
        _("The townspeople cheer as you walk into town."),
        _("{{lb:Look around.}}")
    ]
    commands = [
        "ls"
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]

    file_list = [
        {
            "path": "~/town/Rabbit",
            "contents": get_story_file("Rabbit-cute")
        },
        {
            "path": "~/town/Swordmaster",
            "contents": get_story_file("swordmaster-without-sword")
        }
    ]

    deleted_items = [
        "~/woods/thicket/rabbithole/Rabbit",
        "~/woods/thicket/rabbithole/Swordmaster"
    ]

    def next(self):
        return 46, 7


class Step7(StepTemplateSudo):
    story = [
        _("You see everyone you met on your journey lined up along the street, clapping and cheering."),
        _("Talk to everyone.")
    ]
    start_dir = "~/town"
    end_dir = "~/town"

    hints = [
        _("")
    ]

    all_commands = {
        "cat Mum": _("Mum: {{Bb:I'm so proud of you " + get_username() + "!}}"),
        "cat Dad": _("Dad: {{Bb:You know " + get_username() + "....you've done alright.}}"),
        "cat grumpy-man": _("grumpy-man: {{Bb:\"Ruth told me about how you helped hide her and our animals. "
                            "Thank you!}}"),
        "cat Ruth": _("Ruth: {{Bb:\"If you ever come by the farm, you can have a glass on milk on us!\"}}"),
        "cat little-boy": _("little-boy: {{Bb:\"Mummy is safe!\"}}"),
        "cat young-girl": _("young-girl: {{Bb:\"We found Mummy. I'm really glad she's safe.\"}}"),
        "cat Edith": _("Edith: {{Bb:\"I'm so glad Eleanor is safe! And you too Edward.\"}}"),
        "cat Edward": _("Edward: {{Bb:\"Now all this is over, we can go back to a proper house, instead of living"
                        " in hiding.\"}}"),
        "cat Eleanor": _("Eleanor: {{Bb:\"You found my parents! I knew they would be alright.\"}}"),
        "cat dog": _("dog: {{Bb:\"Woof woof!\"}}"),
        "cat Bernard": _("Bernard: {{Bb:\"Who is that Masked Swordmaster? He looks oddly familiar.\"}}"),
        "cat Clara": _(
            "Clara: {{Bb:\"You found my children! Oh I'm so relieved you two are ok! "
            "Thank you " + get_username() + "\"}}"
        ),
        "cat Swordmaster": _("Swordmaster: {{Bb:\"You should be very proud of what you've achieved. You are indeed"
                             " something to be reckoned with.\"}}"),
        "cat Rabbit": _("Rabbit: {{Bb:....}}"),
        "cat Mayor": _("Rabbit: {{Bb:....}}")
    }

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = _("\n{{gb:You look around.}}")
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            _("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % self.all_commands.keys()[0]
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        if (line in self.all_commands.keys()) and end_dir_validated:
            hint = "\n" + self.all_commands[line]
            self.all_commands.pop(line, None)

            if len(self.all_commands) == 0:
                hint += _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            self.send_hint(hint)
        else:
            self.send_stored_hint()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        self._is_finished = True
        self.exit()
        return -1, -1
