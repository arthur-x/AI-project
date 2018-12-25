# AI-project
The main files are in: AI-project/code/flightgear_control/flightgear_control/
## Updated:

***REWARD function added in communicate.py***

**Note:** If you want files in the previous version, simply click *release* and download version0.<br>

**1.** *main.c* and other files are modified. Right now, the plane would take off following the simple control in *main.c* and only listen to *communicate.py* when altitude is above 4800m.<br>

**2.** A network is trained by *immitate.py* and used in *communicate.py*. The network is trained on data in *data.csv*. Right now, this network's performance is highly unstable, and you would see some interesting behaviors once it's in the sky above 4800m as described...<br>

**3.** By the way, there is a file called *clean.py*. It is used to clean up *in.txt* after every crash of the plane so that bad actions don't get carried into next experiment. You must excute this script at the end of every experiment. You would find it **VERY** helpful.<br>

**4.** **Things to do next:** We still need to build a deep RL algorithm. Currently I have some ideas about writing a reward function using *angle.py* to calculate the heading error and so on, as you can see in *communicate.py*. But it's still pretty primitive. Also, the current goal I think should be **using DRL to control the plane to fly at a given altitude with a given heading angle. But how to achieve it?** Tell me what you think.

## Several things...
1. *data.csv* is a record of one play by the simple strategy in *main.c*.
To use simple strategy, you have to enter test mode.
First modify *main.c* according to the comments inside, then run the simulation.
It would store all data(states) in *test.txt*.
Then run *read_data.py* to convert *test.txt* to csv file.<br>

2. *communicate.py* is the file to communicate with *main.c* via *in.txt* and *out.txt*.
A clearer explanation is shown in the figure *structure.jpg*.<br>
<div align=center><img width="600" height="400" src="https://github.com/arthur-x/AI-project/blob/master/structure.jpg"/></div>
