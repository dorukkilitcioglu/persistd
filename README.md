# persist-desktop
Persist-desktop allows you to persist your virtual desktop over multiple reboots. Automatically open all your relevant programs, and close them when you're done for the day.

## Getting Started

The development will be done using Python 3.7, and I won't be supporting Python 2.x. It's 2018. Come on.

### Prerequisites

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

TODO: There will be instructions to run it using a CLI soon. Right now, you can use `python persist.py -h` to see the options.

There is a _very_ good chance that this requires administrator access, so try using that if you get an error.

### Programs

#### SublimeText (Windows)

In order to use SublimeText, you need to make sure that you [disable auto-reloading of the last session](https://forum.sublimetext.com/t/disable-automatic-loading-of-last-session/4132/15). Right now, the only way around this seems to be using a portable SublimeText.

## Future Plans

Look at the [issues](https://github.com/dorukkilitcioglu/persist-desktop/issues) to see what needs to be done. The first order of business is to get the first milestone working. From there on, more programs and desktops can be added in.

## Contributing

If you see any bugs, or have suggestions, feel free to open up an issue or comment on an existing one. I'm probably not going to accept any pull requests until the first milestone, because the project structure is not yet fixed.

## License
See [LICENSE](LICENSE) for details, but its GPL3. If you build something amazing on top of this, its great, just make sure that its source code is also available under GPL3.

## Author
**[Doruk Kilitcioglu](https://dorukkilitcioglu.github.io/)**
