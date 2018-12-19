# AI-project
The main files are in: AI-project/code/flightgear_control/flightgear_control/
## Several things...
1. *data.csv* is a record of one play by the simple strategy in *main.c*.
To use simple strategy, you have to enter test mode.
First modify *main.c* according to the comments inside, then run the simulation.
It would store all data(states) in *test.txt*.
Then run *read_data.py* to convert *test.txt* to csv file.<br>

2. *communicate.py* is the file to communicate with *main.c* via *in.txt* and *out.txt*.
A clearer explanation is shown in the figure *structure.jpg*.<br>
<div align=center><img width="600" height="400" src="https://github.com/arthur-x/AI-project/blob/master/structure.jpg"/></div>
