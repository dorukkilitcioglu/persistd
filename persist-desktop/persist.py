#!/usr/bin/env python

import argparse
import os
import sys

import settings
from util.command_line import askyn
from util.persister import Persister


def get_all_projects(base_path = settings.BASE_PATH):
    return [d for d in next(os.walk(base_path))[1] if not d.startswith('.')]


# this should never be the name of a project
# if it is, shame on you
DEFAULT_PROJECT = '|||||||'


def main():
    parser = argparse.ArgumentParser(description="Persist your desktop.")
    parser.add_argument('-n', '--new', action='store_true', help="create a new project with the given name")
    parser.add_argument('-c', '--close', action='store_true', help="close & persist the project with the given name")
    parser.add_argument('-d', '--delete', action='store_true', help="delete a project")
    parser.add_argument('-a', '--add', help="add a new program to the project")
    parser.add_argument('-r', '--remove', help="remove a program from the project")
    parser.add_argument('-l', '--list-projects', action='store_true', help="list all projects under the base path")
    parser.add_argument('project_name', nargs='?', default=DEFAULT_PROJECT)
    args = parser.parse_args()

    persister = Persister(settings.BASE_PATH, args.project_name)

    # First, take care of options that don't need the project_name
    if args.list_projects:
        all_projects = get_all_projects()
        for i, project in enumerate(all_projects, start=1):
            print('{0:d}. {1:s}'.format(i, project))
        ind = int(input('Please enter the index of the project you want to launch, or 0 to exit: ')) - 1
        if ind > -1 and ind < len(all_projects):
            project_name = all_projects[ind]
            print('Launching %s' % project_name)
            persister = Persister(settings.BASE_PATH, project_name)
            persister.launch_project()
        elif ind != -1:
            sys.exit('The specified index is not valid.')
    # Then, check if project_name is set
    elif args.project_name and args.project_name != DEFAULT_PROJECT:
        if args.new:
            persister.create_project()
        elif args.close:
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
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
