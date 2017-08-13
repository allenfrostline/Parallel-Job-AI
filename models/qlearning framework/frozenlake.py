# Frozen lake problem: find goal as fast as possible without falling into any hole.
# Map as below:
# ■ ■ ■ ■ ■ ■ ■ ■
# ■     ○       ■
# ■         ○   ■
# ■   ✭   ○     ■
# ■     ○       ■
# ■ ○   ○   ○   ■
# ■ ■ ■ ■ ■ ■ ■ ■
# Reward if goal is arrived, punish if get into an ice hole, stop if knock onto walls or arrive at goal.
# Small punishment after each step, to force the agent go faster.
# Try to change the MAP and hyperparameters in the model.train() method. Parameter tuning is rather tricky.
# For more insight, see qlearning.py and Wikipedia for Q learning.


import numpy as np
from qlearning import network
np.random.seed(2)


# some useful functions
randrow = lambda X: X[np.random.randint(0,len(X))]
samepos = lambda x,y: all(i==j for i,j in zip(x,y))
sumpos = lambda x,y: [i+j for i,j in zip(x,y)]
# map configuration
w,h,g = -.01,-1,10
MAP = np.array([ 
    [w,w,w,w,w,w,w,w],
	[w,0,0,h,0,0,0,w],
	[w,0,0,0,0,h,0,w],
	[w,0,g,0,h,0,0,w],
	[w,0,0,h,0,0,0,w],
	[w,h,0,h,0,h,0,w],
	[w,w,w,w,w,w,w,w],
])
# other settings derived from the map for the model
m,n = MAP.shape
S = np.array(np.where(MAP<np.inf)).T.tolist() # note: it's a mnx2 matrix
S_ = np.array(np.where(MAP==0)).T.tolist() # position where there's no wall, holes or goal
A = [[0,1],[1,0],[0,-1],[-1,0]] # East, South, West and North
f = lambda s,a: [sumpos(s,a), MAP[s[0]+a[0],s[1]+a[1]] - .01] # punishment for redundant steps
initial = lambda S: randrow(S_)
terminal = lambda s: MAP[s[0],s[1]] in [w,g] # stop if knock onto walls or arrive at the goal
# model initializing and training
model = network(S,A,f,initial,terminal)
model.train(alpha=.001,episodes=500000,epsilon=.05,verbose=13,seed=2) # scale of epsilon largely affects iteration speed
# final policy
symbols = {'w':'\u25a0','h':'\u25cb','g':'\u272d',0:'\u2192',1:'\u2193',2:'\u2190',3:'\u2191'}
cell_type = lambda x: 'w'*int(x==w)+'h'*int(x==h)+'g'*int(x==g)
final_policy = lambda Q,s: cell_type(MAP[S[s][0],S[s][1]]) if MAP[S[s][0],S[s][1]]!=0 else np.argmax(Q[s,:])
print('Final policy:')
for i in range(m):
	print(' '.join(['{}'.format(symbols[final_policy(model.Q,n*i+j)]) for j in range(n)]))

