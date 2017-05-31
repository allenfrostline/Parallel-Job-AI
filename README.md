# Parallel Job AI

This is a Tetris-like game with a heuristic-driven AI player. Rather than `Python 3.6`, everything is written is `Python 2.7` due to poor performance of `pygame-c36` on Mac OS.

The original [Tetris game](https://github.com/allenfrostline/Tetris-AI), which has been simplified and implemented with the AI, is based on this [non-AI version](https://gist.github.com/kch42/565419/download).

## Model description

TBD.

<img src='./doc/img/play.png' width=50%/><img src='./doc/img/result.png' width=50%/>

## Dependencies

Requires `pygame` (which isn't on pip). You can download [here](https://bitbucket.org/pygame/pygame/downloads). Apart from this, requires `copy`, `threading`, `random`, `collections` and `numpy`.

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

## License

[MIT License](./LICENSE).
