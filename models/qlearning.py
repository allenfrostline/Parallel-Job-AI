import numpy as np
import matplotlib.pyplot as plt
np.random.seed(222)
np.set_printoptions(linewidth=1000,threshold=np.inf,suppress=True)


class network:
	def __init__(self,S,A,f,initial,terminal):  
		# S: stage space, matrix (single stage being rows)
		# A: action space, matrix (single action being rows)
		# f(s,a): returns next stage & reward
		# initial(S): initial stage, can be random
		# terminal(s): when to terminate the iteration
		self.Q = np.zeros([len(S), len(A)])
		self.S = S
		self.A = A
		self.f = f
		self.initial = initial
		self.terminal = terminal

	def train(self,alpha=0.05,gamma=0.9,episodes=1000,epsilon=0.01,maxiter=100000,verbose=0):
		randrow = lambda X: X[np.random.randint(0,len(X))]
		idx = lambda X,x: X.index(x)
		# alpha: learning rate
		# gamma: discount rate
		# episodes: number of episodes
		# epsilon: exploration rate
		# maxiter: maximum iterations for each episode
		# verbose: 0 or False for no output, 1 or True for iterations, 2 for table, 3 for plot, e.g. verbose=123, verbose=True
		STEP = int(episodes/100)
		verbose = str(int(verbose))
		self.score = []
		self.error = []
		self.score_avg = []
		self.error_avg = []
		for i in range(episodes):
			self.s = self.initial(self.S)
			self.a = self.A[np.argmax(self.Q[idx(self.S,self.s),:])]
			self.score.append(0)
			self.error.append(0)
			k = 0
			while not (self.terminal(self.s) or k>maxiter):
				a_best = self.A[np.argmax(self.Q[idx(self.S,self.s),:])]
				a_random = randrow(self.A)
				a_prime = a_random if (np.random.rand()<epsilon) else a_best
				s_prime,r_prime = self.f(self.s,a_prime)
				s_idx = idx(self.S,self.s)
				a_idx = idx(self.A,self.a)
				sp_idx = idx(self.S,s_prime)
				dQ = alpha * (r_prime + gamma * np.max(self.Q[sp_idx,:]) - self.Q[s_idx,a_idx])
				self.error[-1] = abs(dQ)
				self.Q[s_idx,a_idx] += dQ
				self.a = a_prime
				self.s = s_prime
				self.score[-1] += r_prime
				k += 1
			self.score_avg.append(np.mean(self.score[-STEP*(i>=STEP):]))
			self.error_avg.append(np.mean(self.error[-STEP*(i>=STEP):]))
			if '1' in verbose:
				print('[{}/{}] Score: {:.8f} Error: {:.8f}'.format(i+1,episodes,self.score_avg[-1],self.error_avg[-1]))
		if '2' in verbose:
			print('\nQ table:')
			print(self.Q.round(4))
		if '3' in verbose:
			fig = plt.figure(figsize=(10,10))
			ax1 = fig.add_subplot(211)
			ax1.plot(range(episodes),self.score_avg,'r-')
			plt.ylabel('score')
			plt.xlabel('episodes')
			ax2 = fig.add_subplot(212)
			ax2.plot(range(episodes),self.error_avg,'r-')
			plt.ylabel('error')
			plt.xlabel('episodes')
			plt.show()

