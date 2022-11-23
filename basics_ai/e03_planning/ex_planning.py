import numpy as np
import mdp as util


def print_v_func(k, v):
    if PRINTING:
        print "k={} V={}".format(k, v)


def print_simulation_step(state_old, action, state_new, reward):
    if PRINTING:
        print "s={} a={} s'={} r={}".format(state_old, action, state_new, reward)


def v_step(mdp, v):
    v_kp1 = np.zeros(mdp.num_states)
    for s1 in range(mdp.num_states):
        values = np.zeros(mdp.num_actions)
        for a in range(mdp.num_actions):
            summe = 0
            for s2 in range(mdp.num_states):
                summe += mdp.psas[s2, a, s1] * v[s2]
            values[a] = mdp.ras[a, s1] + mdp.gamma*summe
        v_kp1[s1] = max(values)
    return v_kp1

def q_step(mdp, q):
    qkp1 = np.zeros((mdp.num_states, mdp.num_actions))
    argmax_a = np.amax(q, axis = 1)
    for s1 in range(mdp.num_states):
        for a in range(mdp.num_actions):
            summme = 0.0
            for s2 in range(mdp.num_states):
                summme += mdp.psas[s2, a, s1] * max(q[s2])
            qkp1[s1, a] = mdp.ras[a, s1] + mdp.gamma * summme
    return qkp1

def value_iteration(mdp, num_iterations=10):
    """
    Does value iteration on the given Markov Decision Process for given number of iterations

    :param mdp: the Markov Decision Process
    :param num_iterations: the number of iteration to compute the V-function
    :return: (v, q) = the V-function and Q-function after 'num_iterations' steps

    :type mdp: util.MarkovDecisionProcess
    :type num_iterations: int
    """
    """
     Useful functions:
      - arr = np.ones(shape)
      - arr = np.zeros(shape)
      - arr = np.empty(shape)
      - arr = np.array(list)
      - mdp.gamma
      - P(s'|s,a) = mdp.psas[s',a,s]
      - reward = mdp.ras[a,s]
      - max(arr), util.argmax(arr)
    """
    q = np.zeros((mdp.num_states, mdp.num_actions))
    v = np.zeros(mdp.num_states)
    for k in range(num_iterations):
        print_v_func(k, v)  # print k and v
        #print q
        #using two seperate iterations
        #q1 = q_step(mdp, q1)
        #v1 = v_step(mdp, v1)
        
        #using the fip from the exercices
        for s in range(mdp.num_states):
            for a in range(mdp.num_actions):
                summe = 0.0
                for s2 in range(mdp.num_states):
                    summe += mdp.psas[s2, a, s]*v[s2]
                q[s, a] = mdp.ras[a, s] + mdp.gamma*summe
        for s in range(mdp.num_states):
            v[s] = max(q[s])
    
    
    return v, q

def simulate(mdp, state_old, action):
    """
    Simulates a single step in the given Markov Decision Process
    :param mdp: the Markov Decision Process
    :param action: the Action to be taken
    :param state_old: the old state
    :return: (reward, state_new) = the reward for taking the action in old state and the new state you are in

    :type mdp: util.MarkovDecisionProcess
    :type action: int
    :type state_old: int
    :rtype: tuple
    """
    # this method work as is, no change required
    reward = mdp.ras[action, state_old] # gets reward
    state_new = util.sample_multinomial(mdp.psas[:, action, state_old])  # get new state as sample s' from P(s'|a,s)
    print_simulation_step(state_old, action, state_new, reward)  # print transition and reward
    return reward, state_new

PRINTING = False  # do not print by default, please do not change this
if __name__ == '__main__':
    PRINTING = True  # enable printing
    util.random_seed()  # seed random number generator
    value_iteration(util.data.create_mdp_circle_world_one())
