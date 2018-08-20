import persistd.programs.chrome as chrome
import persistd.programs.conemu as conemu
import persistd.programs.sublime_text as sublime_text

all_programs = [chrome,
                conemu,
                sublime_text,
                ]

code_name_to_class = {program.CODE_NAME: program.PROGRAM_CLASS
                      for program in all_programs
                      if program.PROGRAM_CLASS}

class_to_code_name = {kls: name for name, kls in code_name_to_class.items()}

human_readable_name_to_class = {program.HUMAN_READABLE_NAME: program.PROGRAM_CLASS
                                for program in all_programs
                                if program.PROGRAM_CLASS}

class_to_human_readable_name = {kls: name for name, kls in human_readable_name_to_class.items()}
