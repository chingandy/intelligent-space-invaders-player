import pyautogui
import pickle

class Control:
    def __init__(self):
        self.observation_space = (40, ) # positions of the aliens, position of ship, position of bullets
        self.action_space = (3, ) # Only 3 actions: left, right, fire
        self.training_time = 100  # limit the time for each training session
        self.remaining_time = self.training_time
        self.state_n_reward = None

    def make(self):
        """Preparing the environment, start the game"""
        pyautogui.hotkey('r')



    def reset(self):
        """Reset the game"""
        pyautogui.hotkey('r')
        file = open("state.txt", "rb")
        state_n_reward = pickle.load(file)
        next_state = state_n_reward[:-2]
        # reward = state_n_reward[-1]
        # done = False
        return next_state



    def step(self, action):
        """Receive the action of the agent and return (next_state, reward, done, info)"""
        if action == 0:
            pyautogui.hotkey('left')
        elif action == 1:
            pyautogui.hotkey('right')
        elif action == 2:
            pyautogui.hotkey('space')


        file = open("state.txt", "rb")
        try:
            self.state_n_reward = pickle.load(file)
        except EOFError:
            print("EOFError occurred")

        next_state = self.state_n_reward[:-2]
        reward = self.state_n_reward[-2]
        done = self.state_n_reward[-1]

        if done:   # the ship collided with the Aliens
            reward -= 10

        self.remaining_time -= 1
        if self.remaining_time == 0:
            done = True
            self.remaining_time = self.training_time

        return (next_state, reward, done, None)


    def get_observation_space(self):

        return self.observation_space

    def get_action_space(self):
        return self.action_space
