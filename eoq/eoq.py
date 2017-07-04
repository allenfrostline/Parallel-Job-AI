import numpy as np
import matplotlib.pylab as plt
from matplotlib2tikz import save as tikz_save

from matplotlib import style
style.use('ggplot')


D = 4  # demand per period
h = 1  # holding cost per unit per time
p = 20 # selling price per item
K = 10  # order cost
I_max = 20
Q_max = 10  # maximum order size

state_space = list(range(I_max+1))
action_space = list(range(Q_max))


def run(scenario):
    lr = scenario['lr']
    y = scenario['y']
    num_episodes = scenario['num_episodes']
    length_episode = scenario['length_episode']
    beta = scenario['beta']

    np.random.seed(3)
    Q = np.zeros([len(state_space), len(action_space)])

    # Trace of optimal decisions
    trace = np.zeros([num_episodes, len(state_space)])

    for i in range(num_episodes):
        I = 0
        thres = beta(i)
        for _ in range(length_episode):
            if np.random.rand(1) < thres:
                u = np.argmax(Q[I, :])
            else:
                u = np.random.choice(action_space)
            S = min(I + u, D)  # sales
            I1 = min(I + u - S, I_max)
            R = p*S - h*I1 - K*(u>0)

            #  Update Q-Table with new knowledge
            Q[I, u] += lr*(R + y*np.max(Q[I1, :]) - Q[I, u])
            I = I1

        # keep trace
        trace[i,:] = np.argmax(Q, axis=1)

    np.set_printoptions(precision=3)
    print("Final Q-Table Values")
    print(Q)
    print(np.argmax(Q, axis=1))

    EOQ = np.sqrt(2*K*D/h)
    print("EOQ: ", EOQ)

    fig = plt.figure()
    for i in action_space:
        plt.plot(trace[:,i], 'o-', markersize=2, label=i)
    plt.xlabel('episode')
    # plt.title('Demand and demand during leadtime')
    plt.grid(True)
    plt.legend(loc='center right')
    plt.show()
    fname = 'eoq_learning_{}.tex'.format(scenario['name'])
    # tikz_save(fname, figureheight='5cm', figurewidth='12cm')

def max_total(scenario):
    # maximize the total reward during a finite horizon
    num_episodes = scenario['num_episodes']
    length_episode = scenario['length_episode']
    beta = scenario['beta']

    np.random.seed(3)
    Q = np.zeros([len(state_space), len(action_space)])

    for i in range(num_episodes):
        I = 0
        alpha = 0.99
        thres = beta(i)
        for _ in range(length_episode):
            if np.random.rand(1) < thres:
                u = np.argmax(Q[I, :])
            else:
                u = np.random.choice(action_space)
            D = np.random.randint(3,5)
            #D = 4
            S = min(I + u, D)  # sales
            I1 = min(I + u - S, I_max)
            R = p*S - h*I1 - K*(u>0)

            #  Update Q-Table with new knowledge
            Q[I, u] = R + alpha*np.max(Q[I1, :])
            I = I1
    return Q


# Set learning parameters
scenario_1 = {
    'name': "scenario_1",
    'lr': .85,
    'y': .99,
    'length_episode': 100,
    'num_episodes': 2000,
    'beta': lambda x: 0.8
    #'beta': lambda x: 0.8 + 0.2*x/2000
    }

#run(scenario_1)

scenario_2 = {
    'name': "scenario_2",
    'length_episode': 1000000,
    'num_episodes': 1,
    'beta': lambda x: 0.8
    #'beta': lambda x: 0.8 + 0.2*x/2000
    }

Q = max_total(scenario_2)
np.set_printoptions(precision=3)
print("Final Q-Table Values")
print(Q)
print(np.argmax(Q, axis=1))


