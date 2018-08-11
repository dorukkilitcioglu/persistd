#!/usr/bin/env python

import argparse
import os
import shutil
import sys

import desktops
import programs
import settings
from util.command_line import askyn
from util.persistable import Persistable
from util.savers import save_dict_to_json, load_dict_from_json


class Persister(Persistable):

    @property
    def project_path(self):
        return os.path.join(self.base_path, self.project_name)

    @property
    def persister_folder_path(self):
        return os.path.join(self.project_path, '.persist-desktop')

    @property
    def persister_obj_path(self):
        return os.path.join(self.persister_folder_path, 'pd.json')

    def __init__(self, base_path, project_name):
        """ Initializes a persister that takes care of project files

        Args:
            base_path::str
                The path to the base directory of all projects
            project_name::str
                The name of the project
        """
        # the path to the base directory of all projects
        self.base_path = base_path
        # the name of the project
        self.project_name = project_name
        # the desktop being used
        self.used_desktop = None
        # the desktop object
        self.used_desktop_obj = None
        # the programs being used
        self.used_programs = []
        # the program objects
        self.used_program_objs = {}

        if os.path.exists(self.persister_obj_path):
            self.load()

    def _initialize_project(self):
        # Initialize a desktop
        if len(desktops.all_desktops) == 0:
            sys.exit("Can't find any desktops for your OS. Contact the developer.")
        print('Available desktops are:')
        for i, desktop in enumerate(desktops.all_desktops):
            print("%d. %s" % (i + 1, desktop.HUMAN_READABLE_NAME))
        desktop_index = int(input('Please select the desktop you want to use: ')) - 1
        try:
            desktop = desktops.all_desktops[desktop_index]
        except IndexError:
            sys.exit('Please select a valid desktop!')
        self.used_desktop = desktop.CODE_NAME
        self._initialize_desktop_obj()

        # Initialize the programs
        print("Please say y if you want to use a program, n if you don't")
        for program in programs.all_programs:
            if askyn(program.HUMAN_READABLE_NAME):
                self.used_programs.append(program.CODE_NAME)

        self._initialize_program_objects()
        # Set everything up
        self.setup()
        # Save the project
        self.save()
        print("Project successfully initialized.")
        if askyn("Do you want to open the project?"):
            self.launch_project()

    def _initialize_desktop_obj(self):
        """ Initializes the desktop object using the `self.used_desktop` string
        """
        Desktop = desktops.code_name_to_class[self.used_desktop]
        persist_path = os.path.join(self.persister_folder_path, self.used_desktop)
        self.used_desktop_obj = Desktop(self.project_name, self.project_path, persist_path)

    def _initialize_program_obj(self, program_name):
        """ Initializes a program object using `program_name` string
        """
        Program = programs.code_name_to_class[program_name]
        persist_path = os.path.join(self.persister_folder_path, program_name)
        program = Program(self.project_name, self.project_path, persist_path, self.used_desktop_obj)
        self.used_program_objs[program_name] = program
        return program

    def _initialize_program_objects(self):
        """ Initializes multiple program objects
        """
        for program_name in self.used_programs:
            self._initialize_program_obj(program_name)

    def create_project(self):
        """ Creates a new project. See _initialize_project for how to
        initialize a project.
        """
        warnings = ("\nWARNING:\n"
                    "Before creating a project, make sure that you have followed the install instructions.\n"
                    "They can be found at: https://github.com/dorukkilitcioglu/persist-desktop#getting-started\n"
                    "Specifically, make sure you edit the settings to have BASE_PATH pointing to a folder\n"
                    "and the program paths pointing to their relevant executables\n"
                    "If any operation files due to permissions, make sure you run the script with admin rights.\n"
                    )
        print(warnings)

        if os.path.exists(self.project_path):
            # Path exists, see if a persist desktop project has been initialized there
            if os.path.exists(self.persister_folder_path):
                # Project has been initialized before
                sys.exit("Error: project with the name %s already exists" % self.project_name)
            elif askyn("Folder %s already exists, do you want to turn it into a persist-desktop project?" % self.project_name):
                return self._initialize_project()
            else:
                sys.exit("I don't think you really want to create this project...")
        else:
            os.makedirs(self.persister_folder_path)
            return self._initialize_project()

    def add_program_to_project(self, program_name):
        """ Adds a program to the project
        """
        if os.path.exists(self.persister_folder_path):
            if program_name in [program.CODE_NAME for program in programs.all_programs]:
                if program_name in self.used_programs:
                    print('Program is already being used')
                else:
                    self.used_programs.append(program_name)
                    program = self._initialize_program_obj(program_name)
                    program.setup()
                    self.save()
                    print('Program successfully added to %s' % self.project_name)
            else:
                sys.exit("No program with codename %s is available." % program_name)
        else:
            sys.exit("Error: project with the name %s does not exist" % self.project_name)

    def launch_project(self):
        """ Opens a project
        """
        if os.path.exists(self.persister_folder_path):
            self.used_desktop_obj.create_desktop()
            self.used_desktop_obj.switch_to_desktop()
            for program_name, program_obj in self.used_program_objs.items():
                program_obj.start()
            self.save()
        else:
            sys.exit("Error: project with the name %s does not exist" % self.project_name)

    def remove_program_from_project(self, program_name):
        """ Removes a program from the project
        """
        if os.path.exists(self.persister_folder_path):
            if program_name in self.used_programs:
                self.used_programs.remove(program_name)
                program = self.used_program_objs[program_name]
                program.destroy()
                self.save()
                print('Program successfully deleted from %s' % self.project_name)
            else:
                sys.exit("The program with codename %s is not being used." % program_name)
        else:
            sys.exit("Error: project with the name %s does not exist" % self.project_name)

    def close_project(self):
        """ Closes a project
        """
        if os.path.exists(self.persister_folder_path):
            for program_name, program_obj in self.used_program_objs.items():
                program_obj.close()
            self.used_desktop_obj.close_desktop()
            self.save()
        else:
            sys.exit("Error: project with the name %s does not exist" % self.project_name)

    def delete_project(self):
        """ Deletes a project, given user input
        """
        if not os.path.exists(self.project_path):
            sys.exit("Error: project with the name %s does not exist" % self.project_name)
        elif os.path.exists(self.persister_folder_path) and askyn("Do you want to keep the project files?"):
            # only delete persist-desktop files
            self.destroy()
            shutil.rmtree(self.persister_folder_path)
            print("Deleted project files.")
        elif askyn("Are you sure you want to delete all files? This action cannot be undone!"):
            # delete all files
            self.destroy()
            shutil.rmtree(self.project_path)
            print("Deleted all files.")
        else:
            # chickened out
            print("Project not deleted.")

    def setup(self):
        """ Sets up the desktop and all the programs
        """
        self.used_desktop_obj.setup()
        for used_program_key, used_program in self.used_program_objs.items():
            used_program.setup()

    def destroy(self):
        """ Destroys the desktop and all the programs
        """
        for used_program_key, used_program in self.used_program_objs.items():
            used_program.destroy()
        if self.used_desktop_obj:
            self.used_desktop_obj.destroy()

    def save(self, path=None):
        """ Saves the variables to json
        """
        path = path or self.persister_obj_path
        save_dict_to_json(self, path, ['used_desktop_obj', 'used_program_objs'])
        if self.used_desktop:
            self.used_desktop_obj.save()
        for program_name, program_obj in self.used_program_objs.items():
            program_obj.save()

    def load(self, path=None):
        """ Loads variables from json
        """
        path = path or self.persister_obj_path
        load_dict_from_json(self, path)
        if self.used_desktop:
            self._initialize_desktop_obj()
        self._initialize_program_objects()
        if self.used_desktop:
            self.used_desktop_obj.load()
        for program_name, program_obj in self.used_program_objs.items():
            program_obj.load()


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
        for project in get_all_projects():
            print(project)
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
