# Intention estimation and cognitive emulation for military decision making

This is a research project under DRDO(**Defence Research and Development Organization**), India.  
In this research, we have to emulate a pursuit evasion scenario wherein both, the pursuer and the evader are autonomous agents artificially equipped with intelligence.  
This study aims at evolving models for decision making scenarios such as habitat selection, ambush avoidance and dilemma resolution. The study explores optimal situational scenarios wherein deception is likely to be employed. It proposes a model for employing deception through asymmetric false signaling and evaluates its veracity through intention based assessment. The intention based model enables emulation of the proposed signaling using a probabilistic belief structure. Further the control theory based intention model can be employed for mind reading to judge the opponent's intention to deceive.  
More here: [Game Theoretic Cognitive Strategies for Deceptive Military Decision Making](https://github.com/Pankaj-Baranwal/DRDO-Robot/blob/master/DRDO%20Brain/Game%20Theoretic%20Cognitive%20Strategies%20for%20Deceptive%20Report%202016Military%20Decision%20Making.docx?raw=true)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them
#### Hardware:
Raspberry Pi  
Firebird-V Atmega 2560 Tank robot  
RPi Camera module  
  
#### Software:
Ubuntu  
Python  
Matlab  
AVR Studio  
AVR Bootloader  
  
### Installing

A step by step series of examples that tell you have to get a development env running  
Build `FireBirdIntegrated/ServoAndLocomotion.c` into a hex file using AVR studio.  
(More details here: https://github.com/akshar100/eyantra-firebird-resources])  
Burn the hex into the Firebird bot using ***AVR Bootloader***  
Raspberry Pi controls the Firebird motors and servos using the ***PORTJ*** pins onboard the bot.  
The python code which needs to be run on pi can be found here: `Python/GPIO Control/main_file.py`
That is it!

## Running the tests

More will be uploaded soon.

## Deployment

Use `RPi Board.jpg` to connect pins on RPi to Firebird-based bot using the configuration mentioned in the comments of Python file present here: `Python/GPIO Control/main_file.py`

## Contributing

Please deploy it first before contacting us for contributing.  
In case of some error, please post an issue first. We will get back to you as soon as possible.

## Authors

* **Karan Dhingra** - *JAVA code* - [kdhingra307](https://github.com/kdhingra307)
* **Pankaj Baranwal** - *Python code, Embedded C code* - [Pankaj-Baranwal](https://github.com/Pankaj-Baranwal)
* **Raghav Singh** - *Arduino code* - [raghav1875](https://github.com/raghav1875)
* **Sanjeev Dubey** - *Matlab Code* - [getsanjeev](https://github.com/getsanjeev)

See also the list of [contributors](https://github.com/Pankaj-Baranwal/DRDO-Robot/contributors) who participated in this project.

## Acknowledgments

* Dr. A. K. Sinha (G-grade scientist at DRDO)
