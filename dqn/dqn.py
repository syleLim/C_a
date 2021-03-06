import tensorflow as tf
import numpy as np
import random
from collections import deque

class DQN:
    # decide size of memory data sets
    # play result = state + action + reward + is_gameover
    REPLAY_MEMORY = 10000
    # size of replay memory when training
    BATCH_SIZE = 32
    # decrease weight of past state
    GAMMA = 0.99
    # number of past memory
    STATE_LEN = 4

    def __init__(self, session, width, height, n_action): # num_action = 4(left, right, front, back)
        self.session = session
        self.n_action = n_action
        #Camera width / height
        self.width = width        #(Camera width)
        self.height = height      #(Camera height)
        
        # Memory? - what is it?
        self.memory = deque()
        # situation of game
        self.state = None

        # Var for state of game
        # game state var
        self.input_X = tf.placeholder(tf.float32, [None, width, height, self.STATE_LEN])
        # action state var
        self.input_A = tf.placeholder(tf.int64, [None])
        # loss var
        self.input_Y = tf.placeholder(tf.float32, [None])

        self.Q = self._build_network('main') # set main network
        self.cost, self.train_op = self._build_op()

        # 학습을 더 잘 되게 하기 위해,
        # For good training, devide Q / target_Q
        self.target_Q = self._build_network('target')

    # training nn
    def _build_network(self, name):
        with tf.variable_scope(name):
            model = tf.layers.conv2d(self.input_X, 32, [4, 4], padding='same', activation=tf.nn.relu)
            model = tf.layers.conv2d(model, 64, [2, 2], padding='same', activation=tf.nn.relu)
            model = tf.contrib.layers.flatten(model)
            model = tf.layers.dense(model, 512, activation=tf.nn.relu)

            Q = tf.layers.dense(model, self.n_action, activation=None)

        return Q

    # cost function
    def _build_op(self):
        # Perform a gradient descent step on (y_j-Q(ð_j,a_j;θ))^2
        one_hot = tf.one_hot(self.input_A, self.n_action, 1.0, 0.0)
        Q_value = tf.reduce_sum(tf.multiply(self.Q, one_hot), axis=1)
        cost = tf.reduce_mean(tf.square(self.input_Y - Q_value))
        train_op = tf.train.AdamOptimizer(1e-6).minimize(cost)

        return cost, train_op

    # refer: https://github.com/hunkim/ReinforcementZeroToAll/
    def update_target_network(self):
        copy_op = []

        main_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='main')
        target_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target')

        # Update network var to copy train network var
        for main_var, target_var in zip(main_vars, target_vars):
            copy_op.append(target_var.assign(main_var.value()))

        self.session.run(copy_op)

    # Geting Action for next frame
    def get_action(self):
        Q_value = self.session.run(self.Q,
                                   feed_dict={self.input_X: [self.state]})

        action = np.argmax(Q_value[0])

        return action

    # Initialize state of current game (with past state)
    def init_state(self, state):
        state = [state for _ in range(self.STATE_LEN)]
        self.state = np.stack(state, axis=2)

    # set remember state update (new state)
    def remember(self, state, action, reward, terminal):
        next_state = np.reshape(state, (self.width, self.height, 1))
        next_state = np.append(self.state[:, :, 1:], next_state, axis=2)

        # save data(state / reward / is_gameover) in memory (= dqn)
        self.memory.append((self.state, next_state, action, reward, terminal))

        # delete past memory
        if len(self.memory) > self.REPLAY_MEMORY:
            self.memory.popleft()

        self.state = next_state

    # Get data for training random sampling
    def _sample_memory(self):
        sample_memory = random.sample(self.memory, self.BATCH_SIZE)

        state = [memory[0] for memory in sample_memory]
        next_state = [memory[1] for memory in sample_memory]
        action = [memory[2] for memory in sample_memory]
        reward = [memory[3] for memory in sample_memory]
        terminal = [memory[4] for memory in sample_memory]

        return state, next_state, action, reward, terminal

    def train(self):
        # Get data memory
        state, next_state, action, reward, terminal = self._sample_memory()

        # Training
        target_Q_value = self.session.run(self.target_Q,
                                          feed_dict={self.input_X: next_state})

        # loss function
        # if episode is terminates at step j+1 then r_j
        # otherwise r_j + γ*max_a'Q(ð_(j+1),a';θ')
        Y = []
        for i in range(self.BATCH_SIZE):
            if terminal[i]:
                Y.append(reward[i])
            else:
                Y.append(reward[i] + self.GAMMA * np.max(target_Q_value[i]))

        self.session.run(self.train_op,
                         feed_dict={
                             self.input_X: state,
                             self.input_A: action,
                             self.input_Y: Y
                         })