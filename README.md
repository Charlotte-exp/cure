# CURE experiment
Repeated PD with errors implemented in oTree

oTree documentations have all up to date instructions on how to install oTree and run games.
https://otree.readthedocs.io/en/latest/

This version was built and ran with oTree 5.

There are two conditions, one is a normal 20+ round prisoner's dilemma and the other the same game but with 10% errors in implementing player's decisions. 



`oTree5_cure` is an interactive task developed and run with oTree, an open-source platform for web-based interactive economic and psychology experiments. 

- [Overview](#overview)
- [Documentation](#documentation)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Setting up the development environment](#setting-up-the-development-environment)
- [License](#license)
- [Issues](https://github.com/neurodata/mgcpy/issues)

# Overview
``oTree5_cure`` is a two-player interactive task where participants play a repeated prisoner's dilemma over at least 20 rounds. 
A first app called 'introduction' runs the participants through the instructions, assigns them to one of two treatments, and tests their comprehension of the task. 
A second app called 'rpd_errors' pairs participants together based on their treatment and runs them through 20+ rounds of the repeated prisoner's dilemma and calculates payoffs. Once the prisoner's dilemma is over, the participants are redirected to their recruitment platform for payment (Here Prolific).
The two treatments are 'no_errors' and  'with_error'. The first one is a standard repeated prisoner's dilemma. The 'with_error' treatment includes a 10% probability (customisable) that a decision in the game will be implemented wrong. When such an event occurs, the player who 'committed' the error is informed that the error occured, while the other player is not. 

# Documenation
The official oTree documentation with usage is at: http://www.otree.org/
ReadTheDocs: https://otree.readthedocs.io/en/latest/

# System Requirements
## Hardware requirements
`oTree5_cure` requires only a standard computer with enough RAM to support the in-memory operations.

## Software requirements
### OS Requirements
This package is supported for *macOS*, *Windows, and *Linux*. The package has been tested on the following systems:
+ macOS: Catalina (10.15.7)


# Installation Guide:Read

## Installing Python
Download the latest python 3 version at https://www.python.org/downloads/ and follow the official instructions.

## Installing oTree

Enter this command in the computer terminal:

```
pip3 install otree==5.8.5
```

# Running the web-based task:

## Locallly
Download the zip file called `oTree5_cure.otreezip` at https://github.com/cs-dlut/CURE.git.
open the zip and travel to that folder in the Terminal.
enter the command

```
otree devserver
```

Open your browser to http://localhost:8000/.
Select Repeated PD with errors to open a demo session. 

To run a real experiment, go to the session tab and create a session with the desired number of participant.
Copy the session-wide link and share it with the participants
Once the experiment is done, data can be collected under the Data tab in the form of a csv file. 

## On a server

oTree recommends different ways to set up an oTree game on a server here: https://otree.readthedocs.io/en/latest/server/intro.html. 
We used Heroku. 

# License

This project is covered under the **MIT license**.




