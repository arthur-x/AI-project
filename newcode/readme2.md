# This is the new code
1. *core.py* and *buffer.py* are directly copied from openai's PPO. They are for reference. Try to write a PPO similar to it.<br>

2. FightGear environment wrapped in *env.py*, PID control wrapped in *client.py*, *actor_critic.py* defines the networks, 
you are free to modify it. *imitate.py* trains a network *policy.pkl* based on *data.csv*.<br>

3. All the scripts are encapsuled in *communicate.py*, run it and you will see the results. Currently the plane will be controlled by PID
under altitude 4000, and by networks above 4100.
