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