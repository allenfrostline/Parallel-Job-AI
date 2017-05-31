# Parallel Job AI

This is a Tetris-like game with a heuristic-driven AI player. Rather than `Python 3.6`, everything is written is `Python 2.7` due to poor performance of `pygame-c36` on Mac OS. However, on linux it works fine with `Python 3`.

The original [Tetris game](https://github.com/allenfrostline/Tetris-AI), which has been simplified and implemented with the AI, is based on this [non-AI version](https://gist.github.com/kch42/565419/download).

## Model description

In this Tetris game board, each column stands for a production line and each row for a day. For example, the bottom left cell stands for the operation status of line 1 on the next day. Each job requires a certain number of days to process, among which there is one day for several hours of painting. This is symbolized as an `I`-stone in the Tetris game, though with different lengths and two colors. Gray boxes means the production line is in operation but not in painting. Yellow boxes means the job is under painting this day. The factory is faced with a bottleneck for painting, specifically, the daily painting should never exceed 12, which corresponds to the row-sum in the game board, and for certain reasons the longest schedule should not exceed four weeks, restricting the max-height to be no more than 28. Our very basic objective is to survive the game as long as possible.

These are the files:

1. `job.py`: Run this file to play the game.
2. `ai.py`: Main program for the AI player.
3. `heuristic.py`: A list of heuristics.

<img src='./doc/img/play.png' width=50%/><img src='./doc/img/result.png' width=50%/>

## Dependencies

Requires `pygame` (which isn't on `pip`, but certainly works with `pip3`). You can download [here](https://bitbucket.org/pygame/pygame/downloads). Apart from this, requires `copy`, `threading`, `random`, `collections` and `numpy`.

## Usage

How to install and open the game:

```bash
git clone https://github.com/allenfrostline/Parallel-Job-AI
cd Parallel-Job-AI-master
python2.7 ward.py
```

How to play the game:

|KEY|COMMAND|
|---:|:---|
|Down|Drop stone faster|
|Left / Right|Move stone|
|Up|Rotate stone clockwise|
|Escape|Quit this round of game|
|P|Toggle the instant mode for AI|
|Q|Exit the whole game|
|Return|Manual instant drop|
|Space|Replay the game|

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :-)

## History

By far I really can't find much about previous work on similar models. So I'd say it is novel.

## To-do

1. Add more heuristics.
2. Implement the learning part.

## License

[MIT License](./LICENSE).
