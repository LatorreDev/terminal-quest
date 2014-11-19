#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story


from linux_story.Step import Step
from linux_story.terminals.terminal1 import Terminal1
from challenge_2 import Step1 as Step1_2
from linux_story.file_data import copy_data
from linux_story.helper_functions import print_challenge_title


class Step_Template(Step):
    def __init__(self):
        Step.__init__(self)

    def launch_terminal(self):
        Terminal1(self.start_dir, self.end_dir, self.command, self.hint)


class Step1(Step_Template):
    story = [
        "Hello there",
        "{{rW}}{{oe}}{{yl}}{{gc}}{{bo}}{{pm}}{{re}} to"
        " the dark side of the Kano OS.",
        "Type {{yls}} (short for {{yl}}i{{ys}}t) to have a look around.",
        "You are in a dark room."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls"
    hint = ["Type {{yls}} and press Enter to have a look around."]

    def next(self):
        Step2()


class Step2(Step_Template):
    story = [
        "\nThe room is no longer dark. ",
        "You see the door to an office.",
        "{{yls <Directory Name>}} lets you look into the directory",
        "The office door has a window.  Have a look in the office."
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls office", "ls office/"]
    hint = "Type the command {{yls office}}"

    def next(self):
        Step3()


class Step3(Step_Template):
    story = [
        "\nTo save yourself some typing, press TAB to complete commands",
        "For example, type {{yls of}}, then press TAB.  "
        "Enter the resulting command"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls office", "ls office/"]
    hint = [
        "Pressing TAB should autocomplete the command,"
        " so you should enter the command ls office/"
    ]

    def next(self):
        Step4()


class Step4(Step_Template):
    story = [
        "\nYou can see the files and directories available in this directory",
        "Files are shown in white, directories in blue",
        "The {{bfiling-cabinet}} has a drawer slightly ajar, "
        "it looks like it contains some important folders.",
        "Have a look and see what it contains."
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls office/filing-cabinet", "ls office/filing-cabinet/"]
    hint = [
        "Remember that {{yls <directory name>}} "
        "{{yl}}i{{ys}}ts the files inside a directory",
        "You need to look through the {{boffice}} window into the {{bfiling-cabinet}}",
        "Type {{yls office/filing-cabinet}} and press Enter"
    ]

    def next(self):
        Step5()


class Step5(Step_Template):
    story = [
        "\nYou see two leather bound lever arch files",
        "The one labelled {{bspells}} looks brand new, while "
        "the {{bmissions}} lever-arch looks more battered",
        "Have a look in the {{bmissions}} directory.",
        "To save typing, try pressing UP to replay previous commands."
    ]
    start_dir = "~"
    end_dir = "~"
    command = [
        "ls office/filing-cabinet/missions",
        "ls office/filing-cabinet/missions/"
    ]
    hint = [
        "You need to look through the {{boffice}} window, into the {{bfiling-cabinet}} "
        "and into the {{bmissions}} directory",
        "Type {{yls office/filing-cabinet/missions}} and press Enter"
    ]

    def next(self):
        Step6()


class Step6(Step_Template):
    story = [
        "\nYou see a paper report titled {{grabbit-report}}.",
        "It has TOP SECRET stamped in the corner",
        "To read a file, you use the command {{ycat <filename>}}",
        "Remember, you can use TAB to complete a command"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "cat office/filing-cabinet/missions/rabbit-report"
    hint = [
        "The file is in the {{boffice}}, in the {{bfile-cabinet}} "
        "and in the {{bmissions}} lever arch",
        "Type {{ycat office/filing-cabinet/missions/rabbit-report}} "
        "to read the rabbit report"
    ]

    def next(self):
        Step7()


class Step7(Step_Template):
    story = [
        "You get the feeling there is something hidden in the office",
        "To view hidden files and directories, "
        "use the command {{yls -a <Directory-name>}} (to {{yl}}i{{ys}}t {{ya}}ll) "
        "the files in a directory"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls -a office", "ls -a office/"]
    hint = [
        "Type {{yls -a office}} and press ENTER"
    ]

    def next(self):
        Step8()


class Step8(Step_Template):
    story = [
        "Hidden files start with . and cannot normally be seen",
        "You notice the {{g.sticky_note}} on the desk.",
        "The command {{ycat}} will allow you "
        "to read what's written on the note"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["cat office/.sticky_note"]
    hint = [
        "Type {{ycat office/.sticky_note}} to see what's written on the note."
    ]

    def next(self):
        Step9()


class Step9(Step_Template):
    story = [
        "Lastly, you decide you want to clean up your screen.",
        "The command {{yclear}} clears the writing on the terminal"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "clear"
    hint = [
        "Type {{yclear}} to clear the Terminal."
    ]

    def next(self):
        copy_data(2)
        print_challenge_title("2")
        Step1_2()