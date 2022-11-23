import matplotlib.pyplot as plt
import numpy as np
from environment import environment

def eps_greedy_action(Q, s, eps):
    '''
    Implement epsilon greedy action selection:
        With Probability 1-eps select greedy action,
        otherwise select random action

    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s: state 
    :type s: int 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    
    :returns: selected action
    :rtype: int
    '''
    if np.random.rand() > eps:
        return np.argmax(Q[s, :]) 
    else:
        return np.random.randint(0, Q.shape[1]) 


def smooth(y, box_pts):
    '''
    Simple box filter implementation for smoothing
    
    :param y: discrete signal to be smoothed
    :type gamma: npumpy.ndarray
    
    :returns: smoothed signal 
    :rtype: numpy.ndarray
    '''

    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def qlearning(Q, s0, env, alpha, gamma, eps, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type eps: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    #pass
    
    reward_list = np.zeros(episodes)
    
    for e in range(episodes):
        current_s = s0
        while current_s != env.goal:
            choosen_a = eps_greedy_action(Q, current_s, eps)
            next_s, reward = env.apply_action(current_s, choosen_a)
            Q[current_s, choosen_a] += alpha*(reward + gamma*max(Q[next_s]) - Q[current_s,choosen_a])
            current_s = next_s
            reward_list[e] += reward
    return Q, reward_list

def sarsa(Q, s0, env, alpha, gamma, eps, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    #pass
    
    reward_list = np.zeros(episodes)
    
    for e in range(episodes):
        current_s = s0
        choosen_a = eps_greedy_action(Q, current_s, eps)
        
        while current_s != env.goal:
            next_s, reward = env.apply_action(current_s, choosen_a)
            next_a = eps_greedy_action(Q, next_s, eps)
            Q[current_s, choosen_a] += alpha*(reward + gamma*Q[next_s, next_a] - Q[current_s,choosen_a])
            current_s = next_s
            choosen_a = next_a
            reward_list[e] += reward 
    return Q, reward_list

def qlearning_sched(Q, s0, env, alpha, gamma, eps0, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type eps: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    #pass
    reward_list = np.zeros(episodes)
    e_step = (eps0-0.1)/float(episodes)

    for e in range(episodes):
        eps = eps0-e_step*e
        current_s = s0
        while current_s != env.goal:
            choosen_a = eps_greedy_action(Q, current_s, eps)
            next_s, reward = env.apply_action(current_s, choosen_a)
            Q[current_s, choosen_a] += alpha*(reward + gamma*max(Q[next_s]) - Q[current_s, choosen_a])
            current_s = next_s
            reward_list[e] += reward
    return Q, reward_list


def sarsa_sched(Q, s0, env, alpha, gamma, eps0, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    #pass
    reward_list = np.zeros(episodes)
    e_step = (eps0-0.1)/float(episodes)

    for e in range(episodes):
        eps = eps0-e_step*e
        current_s = s0
        choosen_a = eps_greedy_action(Q, current_s, eps)
        
        while current_s != env.goal:
            next_s, reward = env.apply_action(current_s, choosen_a)
            next_a = eps_greedy_action(Q, next_s, eps)
            Q[current_s, choosen_a] += alpha*(reward + gamma*Q[next_s, next_a] - Q[current_s,choosen_a])
            current_s = next_s
            choosen_a = next_a
            reward_list[e] += reward
    return Q, reward_list

def rmax(Q, s0, env, alpha, gamma, episodes):
    '''
    Implementation of the rmax-like algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    reward_list = np.zeros(episodes)
    eps = 0.1
    count = np.zeros(Q.shape)
    for e in range(episodes):
        current_s = s0
        while current_s != env.goal:
            choosen_a = eps_greedy_action(Q, current_s, eps)
            next_s, reward = env.apply_action(current_s, choosen_a)
            #this is the rmax part
            #if the current sate was visited not often enough
            #use r_max = 0 as reward
            #else use r_max = r(s,a) wich was recieved in line 250
            if count[current_s, choosen_a] < 100:   #!!r!!
                reward = 0                          #!!r!!
            Q[current_s, choosen_a] += alpha*(reward + gamma*max(Q[next_s]) - Q[current_s, choosen_a])
            count[current_s, choosen_a] += 1
            reward_list[e] += reward
            current_s = next_s
    return Q, reward_list

if __name__ == "__main__":
    env = environment()
    
    #Params
    episodes = 5000
    alpha = .1
    gamma = 1.
    eps = 0.1
    eps0 = 1.
    s0 = 36
    
    Q_ql, R_ql = qlearning(np.zeros((48, 4)), s0, env, alpha, gamma, eps, episodes)
    Q_sa, R_sa = sarsa(np.zeros((48, 4)), s0, env , alpha, gamma, eps, episodes)
    Q_ql_sched, R_ql_sched = qlearning_sched(np.zeros((48, 4)), s0, env, alpha, gamma, eps0, episodes)
    Q_sa_sched, R_sa_sched = sarsa_sched(np.zeros((48, 4)), s0, env , alpha, gamma, eps0, episodes)
    Q_rm, R_rm = rmax(np.zeros((48, 4)), s0, env , alpha, gamma, episodes)

    print("Q_Learning")
    env.print_greedy_policy(Q_ql)
    print("Sarsa")
    env.print_greedy_policy(Q_sa)
    print("Q_Learning with scheduled eps")
    env.print_greedy_policy(Q_ql_sched)
    print("Sarsa with scheduled")
    env.print_greedy_policy(Q_sa_sched)
    print("Rmax")
    env.print_greedy_policy(Q_rm)

    np.savetxt("R_ql.csv", R_ql)
    np.savetxt("R_sa.csv", R_sa)
    np.savetxt("R_ql_sched.csv", R_ql_sched)
    np.savetxt("R_sa_sched.csv", R_sa_sched)
    np.savetxt("R_rm_2.csv", R_rm)

    plt.plot(smooth(R_ql, 50), label='Q-Learning')
    plt.plot(smooth(R_sa, 50), label='Sarsa')
    plt.plot(smooth(R_ql_sched, 50), label='Q-Learning with scheduled eps')
    plt.plot(smooth(R_sa_sched, 50), label='Sarsa with scheduled eps')
    plt.plot(smooth(R_rm, 50), label='Rmax')

    
    plt.legend(loc=4)
    plt.show()
