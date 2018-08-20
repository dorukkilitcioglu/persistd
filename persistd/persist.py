#!/usr/bin/env python

import argparse
import os
import sys

import persistd.programs as programs
import persistd.settings as settings
from persistd.util.command_line import askyn
from persistd.util.persister import DEFAULT_PROJECT_NAME, Persister


def get_all_projects(base_path = settings.BASE_PATH):
    return [d for d in next(os.walk(base_path))[1] if not d.startswith('.')]


ACTION_LIST_PROJECTS = 'list-projects'
ACTION_NEW = 'new'
ACTION_OPEN = 'open'
ACTION_CLOSE = 'close'
ACTION_DELETE = 'delete'
ACTION_ADD = 'add'
ACTION_REMOVE = 'remove'
ACTION_INTERACTIVE = 'interactive'
ALL_ACTIONS = [ACTION_LIST_PROJECTS, ACTION_NEW, ACTION_OPEN, ACTION_CLOSE, ACTION_DELETE,
               ACTION_ADD, ACTION_REMOVE, ACTION_INTERACTIVE]
# actions that operate on a project
PROJECT_ACTIONS = [ACTION_OPEN, ACTION_CLOSE, ACTION_DELETE, ACTION_ADD, ACTION_REMOVE]
# actions that operate on programs
PROGRAM_ACTIONS = [ACTION_ADD, ACTION_REMOVE]


def get_action():
    """ Cooses an action or exits
    """
    print('Available actions:')
    actions = [
        "List all projects under the base path",
        "Create a new project",
        "Open a project",
        "Close & persist a project",
        "Delete a project",
        "Add a new program to a project",
        "Remove a program from a project",
    ]

    for i, action in enumerate(actions, start=1):
        print('{0:d}. {1:s}'.format(i, action))

    ind = int(input('Please enter the index of the action you want, or 0 to exit: ')) - 1
    if ind > -1 and ind < len(actions) - 1:
        return ALL_ACTIONS[ind]
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def get_project():
    """ Chooses a project or exits
    """
    print('Available projects:')
    all_projects = get_all_projects()
    for i, project in enumerate(all_projects, start=1):
        print('{0:d}. {1:s}'.format(i, project))
    ind = int(input('Please enter the index of the project you want to launch, or 0 to exit: ')) - 1
    if ind > -1 and ind < len(all_projects):
        return all_projects[ind]
    elif ind == -1:
        sys.exit(0)
    else:
        sys.exit('The specified index is not valid.')


def get_program():
    """ Chooses a program or exits
    """
    print('Available programs:')
    for i, program in enumerate(programs.all_programs, start=1):
        print('{0:d}. {1:s}'.format(i, program.HUMAN_READABLE_NAME))
    ind = int(input('Please enter the index of the program you want to modify, or 0 to exit: ')) - 1
    if ind > -1 and ind < len(programs.all_programs):
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


def main(args):
    persister = Persister(settings.BASE_PATH, args.project_name)

    # First, take care of options that don't need the project_name
    if args.interactive:
        interactive()
    elif args.list_projects:
        project_name = get_project()
        print('Launching %s' % project_name)
        persister = Persister(settings.BASE_PATH, project_name)
        persister.launch_project()
    elif args.new:
        persister.create_project()
    # Then, check if project_name is set
    elif args.project_name and args.project_name != DEFAULT_PROJECT_NAME:
        if args.close:
            persister.close_project()
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
    parser.add_argument('-i', '--interactive', action='store_true', help="start interactive mode")
    parser.add_argument('-n', '--new', action='store_true', help="create a new project")
    parser.add_argument('-o', '--open', action='store_true', help="open a project")
    parser.add_argument('-c', '--close', action='store_true', help="close & persist the project")
    parser.add_argument('-d', '--delete', action='store_true', help="delete a project")
    parser.add_argument('-a', '--add', help="add a new program to the project")
    parser.add_argument('-r', '--remove', help="remove a program from the project")
    parser.add_argument('-l', '--list-projects', action='store_true', help="list all projects under the base path")
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
