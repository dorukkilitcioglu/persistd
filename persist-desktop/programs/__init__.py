import programs.conemu as conemu
import programs.sublime_text as sublime_text

all_programs = [sublime_text,
                conemu,
                ]

code_name_to_class = {program.CODE_NAME: program.PROGRAM_CLASS
                      for program in all_programs
                      if program.PROGRAM_CLASS}

class_to_code_name = {kls: name for name, kls in code_name_to_class.items()}

human_readable_name_to_class = {program.HUMAN_READABLE_NAME: program.PROGRAM_CLASS
                                for program in all_programs
                                if program.PROGRAM_CLASS}

class_to_human_readable_name = {kls: name for name, kls in human_readable_name_to_class.items()}
