#!/usr/bin/env python

import argparse
import sys
from typing import NoReturn, List

import persistd.programs as programs
from persistd.util.projects import get_all_projects
from persistd.util.settings import SETTINGS
from persistd.util.command_line import askyn
from persistd.util.persister import DEFAULT_PROJECT_NAME, Persister


ACTION_SETTINGS = 'settings'
ACTION_LIST_PROJECTS = 'list-projects'
ACTION_LIST_OPEN = "list-open"
ACTION_NEW = 'new'
ACTION_OPEN = 'open'
ACTION_PERSIST = 'persist'
ACTION_CLOSE = 'close'
ACTION_DELETE = 'delete'
ACTION_ADD = 'add'
ACTION_REMOVE = 'remove'
ACTION_INTERACTIVE = 'interactive'
ALL_ACTIONS = [ACTION_SETTINGS, ACTION_LIST_PROJECTS, ACTION_LIST_OPEN, ACTION_NEW, ACTION_OPEN, ACTION_PERSIST,
               ACTION_CLOSE, ACTION_DELETE, ACTION_ADD, ACTION_REMOVE, ACTION_INTERACTIVE]
# actions that operate on a project
PROJECT_ACTIONS = [ACTION_OPEN, ACTION_PERSIST, ACTION_CLOSE, ACTION_DELETE, ACTION_ADD, ACTION_REMOVE]
# actions that operate on programs
PROGRAM_ACTIONS = [ACTION_ADD, ACTION_REMOVE]


def get_action():
    """ Chooses an action or exits
    """
    print('Available actions:')
    actions = [
        "Update settings",
        "List all projects under the base path",
        "List all open projects",
        "Create a new project",
        "Open a project",
        "Persist a project",
        "Close & persist a project",
        "Delete a project",
        "Add a new program to a project",
        "Remove a program from a project",
    ]

    for i, action in enumerate(actions, start=1):
        print('{0:d}. {1:s}'.format(i, action))

    ind = int(input('Please enter the index of the action you want, or 0 to exit: ')) - 1
    if -1 < ind < len(actions):
        return ALL_ACTIONS[ind]
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def list_projects(project_status: str = 'all') -> List[str]:
    print('Available projects:')
    if project_status == 'all':
        all_projects = get_all_projects()
    elif project_status == 'initialized':
        all_projects = get_all_projects(only_initialized=True)
    elif project_status == 'open':
        all_projects = SETTINGS.open_projects
    else:
        raise ValueError(f"Invalid project status {project_status}!")

    for i, project in enumerate(all_projects, start=1):
        print('{0:d}. {1:s}'.format(i, project))

    return all_projects

def choose_project(all_projects: List[str]) -> str:
    ind = int(input('Please enter the index of the project you want to select, or 0 to exit: ')) - 1
    if -1 < ind < len(all_projects):
        return all_projects[ind]
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def get_project(project_status: str = 'all') -> str:
    """ Chooses a project or exits
    """
    all_projects = list_projects(project_status=project_status)
    return choose_project(all_projects)


def get_program():
    """ Chooses a program or exits
    """
    print('Available programs:')
    for i, program in enumerate(programs.all_programs, start=1):
        print('{0:d}. {1:s}'.format(i, program.HUMAN_READABLE_NAME))
    ind = int(input('Please enter the index of the program you want to modify, or 0 to exit: ')) - 1
    if -1 < ind < len(programs.all_programs):
        return programs.all_programs[ind].CODE_NAME
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def interactive():
    """ Chooses an action, and if necessary, a project and a program
    """
    args = []
    action = get_action()
    args.append('--' + action)
    if action in PROGRAM_ACTIONS:
        print()
        program = get_program()
        args.append(program)
    if action in PROJECT_ACTIONS:
        print()
        project = get_project()
        args.append(project)
    parse_args(args)


def get_setting():
    """ Edits a setting or exits
    """
    print('Available settings:')
    all_settings = list(SETTINGS.field_names())
    for i, setting in enumerate(all_settings, start=1):
        print('{0:d}. {1:s}'.format(i, setting))
    ind = int(input('Please enter the index of the project you want to launch, or 0 to exit: ')) - 1
    if -1 < ind < len(all_settings):
        setting = all_settings[ind]
        setattr(SETTINGS, setting, input("Please enter the new value: "))
        SETTINGS.save()
        print("Input saved.")
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def main(args):
    persister = Persister(SETTINGS.base_path, args.project_name)

    # First, take care of options that don't need the project_name
    if args.interactive:
        interactive()
    elif args.list_open:
        projects = list_projects(project_status='open')
        if askyn("Do you want to close the project?"):
            project_name = choose_project(projects)
            print('Closing %s' % project_name)
            persister = Persister(SETTINGS.base_path, project_name)
            persister.close_project()

    elif args.list_projects:
        project_name = get_project()
        print('Launching %s' % project_name)
        persister = Persister(SETTINGS.base_path, project_name)
        persister.launch_project()
    elif args.settings:
        get_setting()
    elif args.new:
        persister.create_project()
    # Then, check if project_name is set
    elif args.project_name and args.project_name != DEFAULT_PROJECT_NAME:
        if args.close:
            persister.close_project()
        elif args.persist:
            persister.persist_project()
        elif args.delete:
            if askyn("Deleting a project cannot be undone. Are you sure you want to delete %s?" % args.project_name):
                persister.delete_project()
            else:
                print("Project not deleted.")
        elif args.add:
            persister.add_program_to_project(args.add)
        elif args.remove:
            persister.remove_program_from_project(args.remove)
        else:
            persister.launch_project()
    # If we reach this, an incorrect configuration was given
    else:
        print('Error: project_name is required')
        args.parser.print_help()
        sys.exit(1)


def parse_args(args):
    """ Parses command line args into a dictionary and calls main
    """
    parser = argparse.ArgumentParser(description="Persist your desktop.")
    parser.add_argument('-s', '--settings', action='store_true', help="update settings")
    parser.add_argument('-i', '--interactive', action='store_true', help="start interactive mode")
    parser.add_argument('-n', '--new', action='store_true', help="create a new project")
    parser.add_argument('-o', '--open', action='store_true', help="open a project")
    parser.add_argument('-p', '--persist', action='store_true', help="persist (save) a project")
    parser.add_argument('-c', '--close', action='store_true', help="close & persist the project")
    parser.add_argument('-d', '--delete', action='store_true', help="delete a project")
    parser.add_argument('-a', '--add', help="add a new program to the project")
    parser.add_argument('-r', '--remove', help="remove a program from the project")
    parser.add_argument('-l', '--list-projects', action='store_true', help="list all projects under the base path")
    parser.add_argument('-t', '--list-open', action='store_true', help="list all open projects")
    parser.add_argument('project_name', nargs='?', default=DEFAULT_PROJECT_NAME)
    parsed_args = parser.parse_args(args)
    parsed_args.parser = parser
    main(parsed_args)


def main_cmd():
    """ Starts the main process from CLI
    """
    parse_args(sys.argv[1:])


if __name__ == '__main__':
    main_cmd()
