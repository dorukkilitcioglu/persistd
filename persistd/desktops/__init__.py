import persistd.desktops.virtual_desktop as virtual_desktop

all_desktops = [virtual_desktop,
                ]

code_name_to_class = {desktop.CODE_NAME: desktop.DESKTOP_CLASS
                      for desktop in all_desktops
                      if desktop.DESKTOP_CLASS}

class_to_code_name = {kls: name for name, kls in code_name_to_class.items()}

human_readable_name_to_class = {desktop.HUMAN_READABLE_NAME: desktop.DESKTOP_CLASS
                                for desktop in all_desktops
                                if desktop.DESKTOP_CLASS}

class_to_human_readable_name = {kls: name for name, kls in human_readable_name_to_class.items()}
