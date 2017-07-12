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
# from numba import jit
# from matplotlib2tikz import save as tikz_save

from matplotlib import style
style.use('ggplot')
plt.rcParams['axes.facecolor']='#f2f2f2'

np.random.seed(3)
np.set_printoptions(linewidth=1000)
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

h = 1 # holding cost per unit per time
p = 15 # selling price per item
K = 9  # order cost
D_max = 4 # maximum demand
D_min = 0 # minimum demand
ED = (D_max + D_min) // 2 # expected demand
I_max = 20 # maximum iventory size 
Q_max = 10 # maximum order size

# demand function
def D():
    # For stochastic  demand: 
    return np.random.randint(1,10)
    # For stochastic demand: 
    return np.random.randint(1, ED*2-1)
    # For deterministic demand
    # return ED

# inventory levels: 0, ..., I_max 
state_space = np.array(range(I_max+1))

# order quantities: 0, ..., Q_max
action_space = np.array(range(Q_max+1))

# Eliminate impossible orders, i.e., to prevent order sizes such that
# the inventory grows beyond its upper bound.

# Actually, this is a matter of taste. You say that the on hand inventory at the start of the period (i.e.,  on-hand inventory at the end of the previous period plus the order size u)  cannot exceed the inventory space. In the rule below, search for the line with **, I say that the end of period inventory (i.e., start of inventory minus demand) cannot exceed the max inventory level. All in all, its a modeling decision. I think we should stick to one rule: either your proposal, which is fine to me, or mine. In the first case, we can change the ** line to quoted alternative. Its ok if you choose.

def allowed_actions(I):
    tmp = []
    for u in action_space:
        if I + u <= I_max:
            tmp.append(u)
    return np.array(tmp)

def update(I, thres):
    # For given inventory level I, make a choice for the reorder quantity. Store this choice as u. 
    # thres: the acceptance level of the exploration action
    
    # make a choice for the next action 
    if np.random.rand(1) < thres:
        u = np.argmax(Q[I, :])
    else:
        u = np.random.choice(allowed_actions(I))
    # u is the amount we are going to order
    S = min(I + u, D())  # sales
    I1 = min(I + u - S, I_max)  # ** # the inventory level at the end of the period
    #I1 = I + u - S  # the inventory level at the end of the period
    R = p*S - h*I1 - K*(u>0) # the reward

    return u, I1, R

# @jit
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
        trace[i,:] = np.mean(trace[max(i-99,0):i+1,:], axis=0) # print average order size instead
        # print(trace[i,:20].astype(int))

    return trace


def print_result(trace):
    global EOQ
    # print("Final Q-Table Values")
    print(Q)
    # print(np.argmax(Q, axis=1))
    print(trace[-1,:].round(1))

    EOQ = np.sqrt(2*K*ED/h)
    print("EOQ: ", EOQ)


def plot_decision_trace(trace, scenario):
    # Plot the optimal decision (according to the Q values) per state
    # as a function of the period
    n = len(trace)
    fig = plt.figure(figsize=(10,10))
    ax = []
    for t in range(n):
        ax.append(fig.add_subplot(n,1,t+1))
        ax[t].plot([0, scenario['num_episodes']], [EOQ, EOQ], 'k--', label='EOQ', lw=2)
        for i in action_space:
            ax[t].plot(trace[t][:,i], 'o-', markevery=100, label='inventory = {}'.format(i), lw=2, alpha=(.2+.8*(i==0)))
        plt.xlabel('episode')
        plt.ylabel('order size')
        # plt.title('Demand and demand during leadtime')
        plt.grid(True)
        plt.yticks(range(11))
        # move the legend out of the plot
        box = ax[t].get_position()
        ax[t].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax[t].legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=0)
    plt.show()
    # fname = 'eoq_learning_{}.tex'.format(scenario['name'])
    # tikz_save(fname, figureheight='5cm', figurewidth='12cm')


# Set learning parameters
scenario_1 = {
    'name': "scenario_1",
    'lr': .05,
    'y': .99,
    'length_episode': 50, # it turns out that along this axis the convergence is pretty fast, so no need for large lengths
    'num_episodes': 10000, # more episodes correspond with lower learning rate
    'beta': lambda x: 0.6,
    # 'beta': lambda x: 0.6 + 0.4*x/1000
    }

Q = np.zeros([len(state_space), len(action_space)])
trace1 = run(scenario_1)
print('Q tabular, no guidance:')
print_result(trace1)

print('-' * 113)

# Here we can initialize the ordering policy.
# This is an (s,S) policy with s = D_max and S = EOQ.
Q = np.zeros([len(state_space), len(action_space)])
s = D_max
S = int(EOQ)
for i in range(s):
    Q[i,S-i] = 1000

trace2 = run(scenario_1)
print('Q tabular, with guidance:')
print_result(trace2)

plot_decision_trace([trace1, trace2], scenario_1)

