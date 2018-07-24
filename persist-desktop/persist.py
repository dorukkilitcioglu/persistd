import argparse
import os
import shutil
import sys

import settings


class Persister():

    @property
    def project_path(self):
        return os.path.join(self.base_path, self.project_name)

    @property
    def persister_path(self):
        return os.path.join(self.project_path, '.persist-desktop')

    def __init__(self, base_path, project_name):
        """ Initializes a persister that takes care of project files

        Args:
            base_path::str
                The path to the base directory of all projects
            project_name::str
                The name of the project
        """
        self.base_path = base_path
        self.project_name = project_name

    def _initialize_project(self):
        raise NotImplementedError("TODO initialize project")
        # TODO get desktop, loop over programs, store them somewhere

    def create_project(self):
        """ Creates a new project. See _initialize_project for how to
        initialize a project.
        """
        if os.path.exists(self.project_path):
            # Path exists, see if a persist desktop project has been initialized there
            if os.path.exists(self.persister_path):
                # Project has been initialized before
                sys.exit("Error: project with the name %s already exists" % self.project_name)
            elif ask("Folder %s already exists, do you want to turn it into a persist-desktop project?"):
                return self._initialize_project()
            else:
                sys.exit("I don't think you really want to create this project...")
        else:
            os.makedirs(self.persister_path)
            return self._initialize_project()

    def launch_project(self, project_name):
        # TODO actual thing
        from desktops.virtual_desktop import VirtualDesktop
        project_path = os.path.join(settings.BASE_PATH, project_name)
        base_persist_path = os.path.join(project_path, '.persist_desktop')
        vd_persist_path = os.path.join(base_persist_path, 'virtual_desktop')
        vd = VirtualDesktop(project_name, project_path, vd_persist_path)
        vd.setup()
        vd.create_desktop()
        from programs.sublime_text import SublimeText
        sb_persist_path = os.path.join(base_persist_path, 'sublime_text')
        st = SublimeText(project_name, project_path, sb_persist_path, vd)
        return vd, st

    def close_project(self, project_name):
        # TODO actual thing
        print("ccc")

    def delete_project(self):
        """ Deletes a project, given user input
        """
        if not os.path.exists(self.project_path):
            sys.exit("Error: project with the name %s does not exist" % self.project_name)
        elif os.path.exists(self.persister_path) and ask("Do you want to keep the project files?"):
            # only delete persist-desktop files
            shutil.rmtree(self.persister_path)
            print("Deleted project files.")
        elif ask("Are you sure you want to delete all files? This action cannot be undone!"):
            # delete all files
            shutil.rmtree(self.project_path)
            print("Deleted all files.")
        else:
            # chickened out
            print("Project not deleted.")


def ask(question):
    ans = input(question)
    return ans is "y" or ans is "Y"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Persist your desktop.")
    parser.add_argument('-n', '--new', action='store_true', help="create a new project with the given name")
    parser.add_argument('-c', '--close', action='store_true', help="close & persist the project with the given name")
    parser.add_argument('-d', '--delete', action='store_true', help="delete a project")
    parser.add_argument('project_name')
    args = parser.parse_args()

    persister = Persister(settings.BASE_PATH, args.project_name)

    if args.new:
        persister.create_project()
    elif args.close:
        persister.close_project()
    elif args.delete:
        if ask("Deleting a project cannot be undone. Are you sure you want to delete %s?" % args.project_name):
            persister.delete_project()
        else:
            print("Project not deleted.")
    else:
        persister.launch_project()
