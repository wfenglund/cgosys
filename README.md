# CGOSYS

The Casual Gaming Operating SYStem is a retro gaming environment written in Python3. It is effectively a wrapper for emulators to make playing more convenient for the player. The idea is to run the program on top of gnu/linux on something like a Raspberry Pi to make it function like a gaming console.

## Current support
### Consoles
At the moment there is support for Gameboy, Gameboy Color and Gameboy Advance throught the use of VisualBoyAdvance.

### Controllers
Currently, keyboards and PowerA controllers are supported.

## Installation
Installing dependencies and cloning cgosys.

### Dependencies
Installing dependencies on different distros (right now only manjaro is tested).

#### Arch based distro (manjaro):
Python dependencies:
```bash
$ sudo pacman -S python-pygame
```
Emulators:
```bash
$ pamac install vbam-sdl
```
cgosys:
```bash
$ git clone https://github.com/wfenglund/cgosys
$ cd cgosys
```

#### Preparations (optional):
It could be a good idea to store your roms in your home folder. From within the `cgosys/` folder (if `~/Rom_files` exists it will be used by cgosys):
```bash
$ cp Rom_files/ ~/
```
Then add your roms to the various sub folders of `~/Rom_files`.

## Running
When you have your roms in their appropriate console sub folders in either `Rom_files` within the cloned repository or in `~/Rom_files`, you can run:
```bash
$ python cgosys.py
```
