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