July 05. Yang

Thanks, the `eoq.pdf` is really interesting and I'm now reading the `.py` files. I guess we can keep updating this `.md` file for conversations.

---


July 05. Nicky

Sure. Like this a bit of delay in downloading is no problem. Git will handle it.

I just checked your changes to eoq.py. No problem. Just in case you don't know, tizk is a really nice package, although programming in it is hard/strange. Matplot2tikz is really useful. 

----

July 06. Yang

Yeah I know `tikz`. Actually I've been using `tikz` to draw graphs in my lecture notes, and mindmaps for final reviews. The problem is, as you mentioned, it is not user-friendly at all. I'm having an issue importing the `matplot2tikz` package. I'll fixed it on my computer.

---

July 06. Yang

I've just checked into the dependencies of `matplotlib2tikz` and it turned out that the `pillow` package, which is required by it, only supports `py3.4`. I get lucky as I have multiple python environments on my computer and the `sS.py` worked when I use

```python 
python3.4 sS.py
```

I write it down here in case of any future problems.

---

July 06. Yang

I just noticed your `communication.tex` file. It's nice but I think a `.tex` for chatting may be of too much work. Using markdown, there's no need to compile every time. Also, $\LaTeX$ works perfectly here. For your consideration, I recommend the application `Moediter` for effortless markdown editing and previewing on Ubuntu. 

This afternoon, I've read the sections by Bertsekas about approximate dynamic programming, including the section 6.5 on Q-learning. However, I still think the following formula given by Wikipedia is the most informative:

![Q-learning](https://wikimedia.org/api/rest_v1/media/math/render/svg/390d024c2ee2a2c2f709642401a3a7b44f7b2e4e)

As for Flappybird, I find this [repository](https://enhuiz.github.io/flappybird-ql/). The author used javascript but the result is fascinating. It takes less than 2 min to converge.

I'm now really reading through the `sS.py` file.

---

July 6, Nicky

Its ok to remove the communications file after you have read it.

I'll check the flappybird files. 2 minutes is impressive.

Let me know if you have questions about the ss.py file.  I wanted to see how far I can get with this inventory model, because I know the optimal policy, so it is easy to provide the RA (reinforcement algo) with a hint on what a good policy should be.

---

July 07, Yang

Hi. I've read context about s,S policy and the EOQ problem, and yes I agree it's a good starting point. As for the stochastic demand issue, I lowered the learning rate you set (according to my experience in using supervised learning algorithms), and extend the number of episodes. The results seemed quite better.


------------

7/7 NIcky

thanks. Yesterday I read about setting the learning rate to something like the value you changed it to. I think I copied the value in the wrong way from some example code.

Do you know how to get the sS example to something that can be used by keras, or some other library. The reason is to speed up the numerical work. Or doesn't that help?

The sS policy is interesting. To prevent loss it is best to set s to something like the maximal demand (assuming that the demand is bounded), and then order to some S. This S must be related to the cost of ordering and holding cost.

I'll play with the code a bit tonight.

---

July 08, Yang

Unfortunately, all I know about Keras is its Neural Network (NN) part, which I once used in stock price prediction, a supervised learning case. Also, I don't think it is Keras that will help with the numerical part. The problem consists of 3 aspects:

1. Our algorithm in `sS.py` is yet a tabular Q Learning, not a Deep Q Network (DQN), so there won't be any layers or NN related stuff, and thus Keras, or its backend, Google's Tensorflow, will not help. To speed up the training, what comes to me is using `numba` in iterations, etc. 
2. The reason we don't use DQN in `sS.py`, I think, is because it's overly complicated compared with our state and action space. However, for the Tetris-like problem, there are much more possible states and $n$ actions ($n$ for the number of columns), so I guess eventually we need DQN.
3. What's more, yesterday I read a post comparing tabular Q, DQN, Asynchronous Advantage Actor-Critic (A3C) and Evolutionary algorithms in flappybird. It turns out that they are seuqentially better than the previous one -- more effcient to converge. Also, I think the idea of ``teaching'' the agent to learn how to schedule is more similar to the Evolutionary algorithm than Q learning.

What do you think of it?

---

July 08, Yang

I made several changes in `sS.py`, testing the efficiency of initializing the Q tabular with given values. (I think this is what we will do to the Tetris-like one, if we're going to use Q Learning.) The result seems not bad but I'm not sure whether I'm setting the initial values correctly according to the (s,S) policy.

I'll look up the document of `Keras` tonight and hope I can figure out how to switch from tabular Q to deep Q.

--------------

July 12, NIcky

the last couple of days I tried to prove something (for some other paper) that was wrong. Proving something that is wrong is typically hard :-) It took me several days to finally give in, and try to disprove it. That took me just half an hour ...

About the s S problem, for your background: the proof that an s, S type of policy is optimal (for stationary demand, convex inventory cost and ordering cost) was given in 1960 or so. It then took 25 years or so to find an efficient algorithm to actually compute the optimal s and S. Interestingly, it is not a simple problem. Moreover, we can consider joint ordering problems, i.e., an inventory with mutltiple sku's (stock keeping units), and then try to find an optimal policy. This is a much, much harder problem, and has not been solved up to now. Besides this, with multiple items it is easy to get many, many states. Suppose each sku can have 50 states or so. Take 10 sku's, then we have 50^10 states. And if that is still doalbe with tabular learning, we can take 20 sku's...

I don't mind about Q learning or not. It was just my initial idea as complete novice in the field. If you have better ideas, I follow you.

The flappy bird example you showed me is indeed very interesting, and very fast. I wonder how much of flappy bird properties they actually used to make it that smart. One reason (for what it is worth) to chose Q learning was that I thought it can handle many sorts of problems and requires not much understanding (human tuning) of the solution method. Thus, is is a flexible method, and adaptable to other, related, scheduling problems. If it isn't, then let me know. I don't mind about what tool we use, as long as you find it interesting, and we get some results.

You mention numba. I didn't think of this. Perhaps you are right, but as far as I recall, numba is not useful for iterations for queueing and/or inventory systems. It is not possible to use intermediate results of the arrays to compute later elements of the array. (Or am I wrong here?)

I'll check your ss tuning parameters

FYI: I just came across lualatex. With this it is possible to build very nicely laid out graphs with tikz, but also do computations in latex with lua (some programming language similar to python).  In case you are interested, let me know. Then I'll mail you a nice example doc.

for the ss example: can't we use the info obtained by the trace in some way?

I also added a few comments on the ss example. Please check it (it not much) and then remove what is no longer relevant.

Nice plots for the ss policy.

I wonder why it takes so much time before the learning algo to converge to some like the sS policy. If I find time tomorrow, I'll do some simulations to see how sensitive the cost is to the specific values of s and S. I actually guess that the cost is not very sensitive to both s and S, hence it is hard to find (by Q learning) the best s and S. 

---

July 13, Yang

I've been reading stuff about Q learning and Evolutionary Algo, and writing some small scripts for comparison. I hope eventually I can give something in between and can be easily applied to scheduling problems like ours. 

As for `numpy`, I agree with you. I tried it but scarcely did it help. Same with `lru_cache` decorators. Therefore, I think the only way out here is either of these two:

1. Move from tabular Q to Deep Q, which is a similar but actually quite different model.
2. Embed `C` or `C++` functions into where is now iterations in `Python`.

Currently I'm following the second path, just to avoid changing the model.

P.S. I recommend you to check out Google's opeartions research tools. They're written in `C` or `C++` I think, and wrapped for easy using in `Python`. There're no machine learning in the package but the framework is interesting.