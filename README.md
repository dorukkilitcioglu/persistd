<img src="images/logo/persistd.png" alt="persistd logo" width="25%"/>

persistd is a workspace/workflow manager made for multi-tasking developers. It allows you to persist your virtual desktop over multiple reboots. Automatically open all your relevant programs, and close them when you're done for the day. Never fear the Windows updates again.

## Getting Started

The development will be done using Python 3.7, and I won't be supporting Python 2.x. It's 2018. Come on.

### Installation

The requirements and how to install them are specified [below](#requirements). Right now, there is no `setup.py` to install this program. That will come in later, as well as PyPI support. For now, just download this repo to a directory and (for ease of use) make sure your `path` includes the `persistd` directory, so you can call `persist.py` directly.

Once downloaded, you can and **should** modify [default settings](persistd/settings/default.py) to point to your program executables. At minimum, you **must** modify the `BASE_PATH`, which will be the main directory that will contain all your projects. If you don't like to move your existing projects, you can simply symlink them to the directory given by `BASE_PATH`.

Some of the other options in [default settings](persistd/settings/default.py) are already set to the common install locations of the programs. They can be changed at will. The preferred method is to create a `local.py` with the same variables at the same directory, which will take precedence over `default.py`. This should make sure your updates are easy.

### Requirements

The dependencies are listed on **requirements.txt**. The list is _very_ short, so you should be able to install it in your base Python installation and not as part of a virtual environment. You can install the dependencies by running
```
pip install -r requirements.txt
```
If you are a purist and don't want to clutter your Python installation with all of these, you can use `virtualenv` to create a new environment beforehand. If you are like me and use Anaconda for managing your Python installations, you can create a new environment with the requirements by calling
```
conda create --name MyEnvironment --file requirements.txt
```
as per the [instructions](https://conda.io/docs/using/envs.html#create-an-environment).

## Usage

There is a _very_ good chance that this program requires administrator access, so try doing that if you get an error in any of the steps below.

Right now, the only way to interact with the program is through a command line interface. You can use `python persist.py -h` to see the options, which will give you something like this:

```
# python persist.py -h
usage: persist.py [-h] [-i] [-n] [-o] [-c] [-d] [-a ADD] [-r REMOVE] [-l]
                  [project_name]

Persist your desktop.

positional arguments:
  project_name

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     start interactive mode
  -n, --new             create a new project
  -o, --open            open a project
  -c, --close           close & persist the project
  -d, --delete          delete a project
  -a ADD, --add ADD     add a new program to the project
  -r REMOVE, --remove REMOVE
                        remove a program from the project
  -l, --list-projects   list all projects under the base path
```

In general, you can run the interactive mode using
```
python persist.py -i
```
which should give you a human readable interface to interact with the program. I personally have a shortcut that calls `persist.py` with this argument, so I don't have to open up a terminal each time I want to open/close a project.


If you want to go in depth with the terminal options, you can create a new project using
```
python persist.py -n <project_name>
```
which will prompt you to first select a desktop manager, and then ask you about the programs you want to use. See [below](#programs) for specific information about the different programs.

Once a project is created, you can launch that project using
```
python persist.py <project_name>
```
which should create a new desktop and open up any programs you have selected while setting up.

Once you're done with a project, you can close all relevant programs & the desktop using
```
python persist.py -c <project_name>
```
I'd advise against manually closing any of the programs, because their states are only persisted when closing. Right now, the only program that is really affected by this is Chrome, though that might change in the future.

If you're done with a project, you can delete it using
```
python persist.py -d <project_name>
```
This will ask you multiple times if you **really** want to delete that project. You can optionally delete only the persistd files from the project.

The two additional options are `-a` and `-r`, which adds or removes a program with the given name. For example, you can remove ConEmu from a project using
```
python persist.py <project_name> -r conemu
```
The supported program names are `conemu`, `chrome`, and `sublime_text`.

### Programs

#### SublimeText (Windows)

In order to use SublimeText, you need to make sure that you [disable auto-reloading of the last session](https://forum.sublimetext.com/t/disable-automatic-loading-of-last-session/4132/15). Right now, the only way around this seems to be using a portable SublimeText. For those of you lazy people out there, here are the steps:
1. Go to Menu Bar > Preference > Settings (User).
2. Add the following lines to the JSON:
   ```
   {
     "hot_exit": false,
     "remember_open_files": false
   }
   ```

3. ???
4. Profit

There is also a caveat with the current implementation, where if you use the regular `subl` executable to open a file outside of this program, **that Sublime Text window will be replicated when you launch a project**. This is highly sub-optimal, but thats how it is for now.

#### Chrome (Windows)

In order to use Chrome, you first need to install the relevant [extension](persistd/programs/chrome/extension). You can find the steps to install the unpacked extension [here](https://stackoverflow.com/questions/24577024/install-chrome-extension-not-in-the-store). Make sure you point Chrome to the [extension folder](persistd/programs/chrome/extension).

I will make sure to actually release it to Chrome Extension Store (or whatever that's called) after a while.

#### ConEmu (Windows)

ConEmu is a good program. It is easy to work with. It doesn't have any problems because ConEmu is a good boy. We should all strive to be ConEmu.

Seriously though, the only thing you have to do is to create your own [startfile](https://conemu.github.io/en/ConEmuArgs.html#Sample-file-or-task). The included one defaults to a single `cmd` window. After creating the project, modify the default startfile at `<project_path>/.persistd/conemu/<project_name>_startfile.txt`. The next time you launch, ConEmu will use those settings.

## Future Plans

Look at the [issues](https://github.com/dorukkilitcioglu/persistd/issues) to see what needs to be done. The first order of business is to get the first milestone working. From there on, more programs and desktops can be added in.

## Contributing

If you see any bugs, or have suggestions, feel free to open up an issue or comment on an existing one. Since we reached the first milestone, I'm more willing to accept pull requests, but make sure that you roughly follow the coding conventions in the files already included in the repo.

## License
See [LICENSE](LICENSE) for details, but its AGPL3. If you build something amazing on top of this, its great, just make sure that its source code is also available under AGPL3.

## Author
**[Doruk Kilitcioglu](https://dorukkilitcioglu.github.io/)**
