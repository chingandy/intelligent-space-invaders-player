Intelligent Space Invader Player  
==========================================
In this project, a reinforcement learning agent was trained to solve a classic
video game 'Space Invaders'. The reinforcement learning used in this project is Deep Q Network.

![screen shot](https://github.com/chingandy/intelligent-space-invaders-player/blob/master/images/screenshot.png)

## Getting started
In order to play the variant of a classic video game Space Invaders, you will need to install the dependencies first. Run the following command in your terminal:

`pip install -r requirements.txt`

### Dependencies
`pygame, keras, tensorflow, pickle, pyautogui`

## Details   
This project involves mainly three components: the video game (several py files), the learning agent (`dqn_agent.py`) and the API which operates as the interface between the game and the agent. The video game scripts are built with several `.py` files which are implemented with the help of `pygame`, the API was implemented with `pyautogui`, which allows the agent to 'actually' play the game, and last but not least, the learning agent was implemented by using the high-level deep learning framework `keras`, and the learning algorithm used is [Deep Q Network](http://files.davidqiu.com//research/nature14236.pdf).

The reward function is designed as the score gained during the game. When the bullet hits an alien, we or the agent get 50 points. The agent has to learn how to react (go left or right) based on the state at that time. In this game, there are three discrete actions available.

* `left arrow` - move left
* `right arrow` - move right   
* `space key`  - fire a bullet (limit: 3 bullets at the same time)


## How to play
After the dependencies are installed, you can first try out the game by running the
file `space_invaders.py`.

`python space_invaders.py`

## How to train the agent  
You can see how the agent is being trained by running the file `main.py`.

`python main.py`



## Result  
The agent is able to achieve the same high score as we human can. We limited the playing time to 100 game cycles, which is approximately equal to **14** seconds. The final highest score the agent achieve is **450**, which is the same as what I can do with 10 trials.






## Reference
 [Human-level control through deep reinforcementlearning](http://files.davidqiu.com//research/nature14236.pdf).
