import pyautogui


class Control:
    def __init__(self):
        self.observation_space = None # positions of the aliens, position of ship, position of bullets
        self.action_space = (3, ) # Only 3 actions: left, right, fire
        self.training_time = 100

    def make(self):
        """Preparing the environment, start the game"""
        pyautogui.hotkey('r')



    def reset(self):
        """Reset the game"""
        pyautogui.hotkey('r')

    def step(self, action):
        """Receive the action of the agent and return (next_state, reward, done, info)"""
        if action == 0:
            pyautogui.hotkey('left')
        elif action == 1:
            pyautogui.hotkey('right')
        elif action == 2:
            pyautogui.hotkey('space')

    def get_observation_space(self):
        return self.observation_space

    def get_action_space(self):
        return self.action_space
