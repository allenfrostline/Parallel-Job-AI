# Inventory problem: cost minimization with stochastic demand.
# Note: EOQ=sqrt(2*K*D/h) with deterministic demand.
# h: olding cost per unit per period
# p: selling price per unit
# K: fixed order cost
# D: stochastic demand
# I: inventory level
# Q: order quantity
# Z: punishment every time the maximum inventory is exceeded

import numpy as np 
from qlearning import network
np.random.seed(222)


# settings for the model
h,p,K = 1,5,2
Z = 100
I_max = 6
Q_max = 6
D = lambda: np.random.randint(4,5)
S = range(I_max+Q_max+1)
A = range(Q_max+1)
def f(s,a):
	sales = min(s+a,D())
	s_prime = s+a-sales
	r_prime = p*sales-h*s_prime-K*(a>0)-Z*(s_prime>I_max) # NB: punishment
	s_prime = min(s+a-sales,I_max) # inventory cannot exceed I_max
	return s_prime,r_prime
initial = lambda S: 0 # no inventory at beginning
terminal = lambda s: None # iterate until maxiter
# model initialization and training
model = network(S,A,f,initial,terminal)
model.train(episodes=5000,maxiter=100,verbose=23)
# final policy
final_policy = lambda Q,s: np.argmax(Q[s,:])
print('{} {}'.format('inventory','order'))
for s in S[:I_max+1]:
	print('{:>5} {:>7}'.format(s,final_policy(model.Q,s)))
print('\nEOQ = {}'.format(np.sqrt(2*K*D()/h)))