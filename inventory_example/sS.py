# use reinforcement learning to compute the optimal ordering policy.

# For deterministic demand this should be the EOQ value.  More
# specifically, Eventually we should order the EOQ in state 0. When
# the inventory at the end of the period is I>0, and the
# (deterministic) demand D per period is larger than I, then we should
# order the EOQ - I. In essence then, the optimal policy is an s,S
# policy.

# For stochastic demand an (s,S) policy is optimal. With the demand
# function D below we can alternate between choosing deterministic or
# stochastic demand.


# It turns out that the results for stochastic demand are really disappointing. 


import numpy as np
import matplotlib.pylab as plt
# from matplotlib2tikz import save as tikz_save

from matplotlib import style
style.use('ggplot')
plt.rcParams['axes.facecolor']='#f2f2f2'

np.random.seed(3)
np.set_printoptions(linewidth=1000)

h = 1  # holding cost per unit per time
p = 20 # selling price per item
K = 8  # order cost
ED = 4 # E(D)
I_max = 20 # maximum iventory size 
Q_max = 10 # maximum order size

# demand function
def D():
    # For stochastic demand: 
    return np.random.randint(1, ED*2-1)
    # For deterministic demand
    # return ED

# inventory levels: 0, ..., I_max 
state_space = np.array(range(I_max+1))

# order quantities: 0, ..., Q_max
action_space = np.array(range(Q_max+1))

Q = np.zeros([len(state_space), len(action_space)])

# Here  we can initialize the ordering policy.
# This is an (s,S) policy with s = ED and S = 2*ED-1.
# for i in range(ED,2*ED):
# 	Q[i,2*ED-i-1] = 1000


def update(I, thres):
    # For given inventory level I, make a choice for the reorder quantity. Store this choice as u. 
    # thres: the acceptance level of the exploration action
    
    # make a choice for the next action 
    if np.random.rand(1) < thres:
        u = np.argmax(Q[I, :])
    else:
        u = np.random.choice(action_space)
    # u is the amount we are going to order
    S = min(I + u, D())  # sales
    I1 = min(I + u - S, I_max)  # the inventory level at the end of the period
    R = p*S - h*I1 - K*(u>0) # the reward

    return u, I1, R


def run(scenario):
    lr = scenario['lr'] # the learning rate
    y = scenario['y'] # discounting factor
    num_episodes = scenario['num_episodes']
    length_episode = scenario['length_episode']
    beta = scenario['beta'] # exploration rate

    # Keep trace of optimal decisions. Per period, store the optimal Q value.
    trace = np.zeros([num_episodes, len(state_space)])

    for i in range(num_episodes):
        I = 0 # initial inventory level
        thres = beta(i)
        for _ in range(length_episode):
            u, I1, R = update(I, thres)
            #  Update Q-Table with new knowledge
            Q[I, u] += lr*(R + y*np.max(Q[I1, :]) - Q[I, u])
            I = I1

        # keep trace
        trace[i,:] = np.argmax(Q, axis=1)

    return trace


def print_Q():
    np.set_printoptions(precision=3)
    print("Final Q-Table Values")
    print(Q)
    print(np.argmax(Q, axis=1))

    EOQ = np.sqrt(2*K*ED/h)
    print("EOQ: ", EOQ)


def plot_decision_trace(trace, scenario):
    # Plot the optimal decision (according to the Q values) per state
    # as a function of the period

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in action_space[::-1]: # to make the I=0 line on the top
        ax.plot(trace[:,i], '-', label=i, lw=2)
    plt.xlabel('episode')
    # plt.title('Demand and demand during leadtime')
    plt.grid(True)
    plt.yticks(range(11))
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=0)
    plt.show()
    # fname = 'eoq_learning_{}.tex'.format(scenario['name'])
    # tikz_save(fname, figureheight='5cm', figurewidth='12cm')


# Set learning parameters
scenario_1 = {
    'name': "scenario_1",
    'lr': .10,
    'y': .99,
    'length_episode': 500,
    'num_episodes': 2000,
    'beta': lambda x: 0.2, 
    # 'beta': lambda x: 0.8 + 0.2*x/2000
    }

trace = run(scenario_1)
print_Q()
plot_decision_trace(trace, scenario_1)

