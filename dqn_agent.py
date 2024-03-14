import sys
import random
import numpy as np

from learning_api import Control
from matplotlib import pyplot as plt
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

EPISODES = 200  # Maximum number of episodes
START_EPSILON = 0.1
END_EPSILON = 0.002


class DQNAgent:
    # Constructor for the agent (invoked when DQN is first called in main)
    def __init__(self, state_size, action_size):
        self.check_solve = False  #
        self.state_size = state_size
        self.action_size = action_size

        self.discount_factor = 0.95
        self.learning_rate = 0.005
        self.epsilon = START_EPSILON
        self.epsilon_step = 0.00001

        self.batch_size = 32  # Fixed
        self.memory_size = 1000
        self.train_start = 100  # Fixed
        self.target_update_frequency = 1

        # Number of test states for Q value plots
        self.test_state_no = 100

        # Create memory buffer using deque
        self.memory = deque(maxlen=self.memory_size)

        # Create main network and target network (using build_model defined below)
        self.model = self.build_model()
        self.target_model = self.build_model()

        # Initialize target network
        self.update_target_model()

    def build_model(self):
        model = Sequential()
        model.add(
            Dense(
                16,
                input_dim=self.state_size,
                activation="relu",
                kernel_initializer="he_uniform",
            )
        )
        model.add(
            Dense(
                self.action_size, activation="linear", kernel_initializer="he_uniform"
            )
        )
        model.summary()
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))

        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state):

        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
        else:
            q_value = self.model.predict(state)
            action = np.argmax(q_value[0])

        if self.epsilon > END_EPSILON:
            self.epsilon -= self.epsilon_step
        print(f"epsilon: {self.epsilon}")

        return action

    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # Add sample to the end of the list

    # Sample <s,a,r,s'> from replay memory
    def train_model(self):
        if len(self.memory) < self.train_start:  # Do not train if not enough memory
            return
        batch_size = min(
            self.batch_size, len(self.memory)
        )  # Train on at most as many samples as you have in memory
        mini_batch = random.sample(
            self.memory, batch_size
        )  # Uniformly sample the memory buffer
        # Preallocate network and target network input matrices.
        update_input = np.zeros(
            (batch_size, self.state_size)
        )  # batch_size by state_size two-dimensional array (not matrix!)
        update_target = np.zeros(
            (batch_size, self.state_size)
        )  # Same as above, but used for the target network
        action, reward, done = [], [], []  # Empty arrays that will grow dynamically

        for i in range(self.batch_size):
            update_input[i] = mini_batch[i][
                0
            ]  # Allocate s(i) to the network input array from iteration i in the batch
            action.append(mini_batch[i][1])  # Store a(i)
            reward.append(mini_batch[i][2])  # Store r(i)
            update_target[i] = mini_batch[i][
                3
            ]  # Allocate s'(i) for the target network array from iteration i in the batch
            done.append(mini_batch[i][4])  # Store done(i)

        target = self.model.predict(
            update_input
        )  # Generate target values for training the inner loop network using the network model
        target_val = self.target_model.predict(
            update_target
        )  # Generate the target values for training the outer loop target network

        # Q Learning: get maximum Q value at s' from target network

        for i in range(self.batch_size):  # For every batch
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                target[i][action[i]] = reward[i] + self.discount_factor * (
                    np.amax(target_val[i])
                )

        # Train the inner loop network
        self.model.fit(
            update_input, target, batch_size=self.batch_size, epochs=1, verbose=0
        )
        return

    # Plots the score per episode as well as the maximum q value per episode, averaged over precollected states.
    def plot_data(self, episodes, scores, max_q_mean):
        plt.figure(0)
        plt.plot(episodes, max_q_mean, "b")
        plt.xlabel("Episodes")
        plt.ylabel("Average Q Value")
        plt.savefig("qvalues.png")

        plt.figure(1)
        plt.plot(episodes, scores, "b")
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig("scores.png")


if __name__ == "__main__":

    control = Control()
    control.make()

    # Get state and action sizes from the environment
    state_size = control.observation_space[0]
    action_size = control.action_space[0]

    # Create agent, see the DQNAgent __init__ method for details
    agent = DQNAgent(state_size, action_size)

    # Collect test states for plotting Q values using uniform random policy
    test_states = np.zeros((agent.test_state_no, state_size))
    max_q = np.zeros((EPISODES, agent.test_state_no))
    max_q_mean = np.zeros((EPISODES, 1))

    done = True
    for i in range(agent.test_state_no):
        print(f"Test: {i}")
        if done:
            done = False
            state = control.reset()

            state = np.reshape(state, [1, state_size])
            test_states[i] = state
        else:
            action = random.randrange(action_size)
            next_state, reward, done, info = control.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            test_states[i] = state
            state = next_state

    print("End of Test states")

    scores, episodes = [], []  # Create dynamically growing score and episode counters
    for e in range(EPISODES):
        print(f"Episode: {e}")
        done = False
        score = 0
        state = control.reset()  # Initialize/reset the environment
        state = np.reshape(
            state, [1, state_size]
        )  # Reshape state so that to a 1 by state_size two-dimensional array ie. [x_1,x_2] to [[x_1,x_2]]
        # Compute Q values for plotting
        tmp = agent.model.predict(test_states)
        max_q[e][:] = np.max(tmp, axis=1)
        max_q_mean[e] = np.mean(max_q[e][:])

        while not done:

            # Get action for the current state and go one step in environment
            action = agent.get_action(state)
            next_state, reward, done, info = control.step(action)
            next_state = np.reshape(
                next_state, [1, state_size]
            )  # Reshape next_state similarly to state
            # Save sample <s, a, r, s'> to the replay memory
            agent.append_sample(state, action, reward, next_state, done)
            # Training step
            agent.train_model()
            score += reward  # Store episodic reward
            state = next_state  # Propagate state

            if done:
                # At the end of very episode, update the target network
                if e % agent.target_update_frequency == 0:
                    agent.update_target_model()
                # Plot the play time for every episode
                scores.append(score)
                episodes.append(e)

                print(
                    "episode:",
                    e,
                    "  score:",
                    score,
                    " q_value:",
                    max_q_mean[e],
                    "  memory length:",
                    len(agent.memory),
                )

                if agent.check_solve:
                    if np.mean(scores[-min(100, len(scores)) :]) >= 195:
                        print("solved after", e - 100, "episodes")
                        agent.plot_data(episodes, scores, max_q_mean[: e + 1])
                        sys.exit()
    agent.plot_data(episodes, scores, max_q_mean)
