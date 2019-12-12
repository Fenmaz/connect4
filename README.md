# Connect 4
> Trung Nguyen, Hormazd Nadir Godrej and Luke Kim

Class project for CS 229: Machine Learning at Stanford University.

Each directory is a separate package for a task with the Connect 4 game.
* ```play```: play a game of Connect 4 on the terminal 
against yourself (or your friend). It serves as a good starting
point for familiarizing oneself with the game.
* ```classification```: given a board position, predict who will be the winner.
The dataset in use is the UIC and the Kaggle dataset. 
__TODO: add hyperlinks to the datasets__
* ```minimax```: solve the game using the Minimax algorithm.
* ```alpha_zero```: solve the game using the AlphaZero algorithms. 
More details below.


## AlphaZero algorithm

The package ```alpha_zero``` is based on 
1. The publication from DeepMind 
([here](https://www.nature.com/articles/nature16961.pdf))
2. The AlphaZero implementation for Connect4 by @Zeta36
([here](https://github.com/Zeta36/connect4-alpha-zero))
3. The Reversi development based on the AlphaZero paper by @mokemokechicken
([here](https://github.com/mokemokechicken/reversi-alpha-zero)) 

---

## Requirements
Each packages have a different set of requirements, but they all require 
Python 3.

1. ```play```: None

2. ```classification```: Requires ```scikit``` and ```pygame```
```shell script
pip install scikit pygame
```

3. ```minimax```: Requires ```pygame```
```shell script
pip install pygame
```

4. ```alpha_zero```: Requires ```tensorflow```, ```keras``` and ```dotenv```.
```shell script
pip install tensorflow keras python-dotenv
```
To set up Tensorflow as the backend for Keras
```shell script
export KERAS_BACKEND=tensorflow
```

## Usage

1. ```play``` package

To play the game:

```shell script
$ python play/src/connect4.py
```

2. ```classification``` 

To run the logistic regression:

```shell script
$ python classification/src/data_util.py
``` 

The script will download data from the UIC database and run
logistic regression on it.

3. ```minimax```

To play against the Minimax solver:

```shell script
$ python solver/src/minimax_playable.py
```

4. ```alpha_zero```

#### Overview
This AlphaGo Zero implementation consists of three worker `self`, `opt` and `eval`
that can be run in parallel.

* `self` is Self-Play to generate training data by self-play using BestModel.
* `opt` is Trainer to train model, and generate next-generation models.
* `eval` is Evaluator to evaluate whether the next-generation model 
is better than BestModel. If better, replace BestModel.

#### Data

* `data/model/model_best_*`: BestModel.
* `data/model/next_generation/*`: next-generation models.
* `data/play_data/play_*.json`: generated training data.
* `logs/main.log`: log file.

#### Use the package

```bash
python src/connect4_zero/run.py self
```

When executed, Self-Play will start using BestModel.
If the BestModel does not exist, new random model will be created and become BestModel.

Options:
* `--new`: create new BestModel
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)

```bash
python src/connect4_zero/run.py opt
```

When executed, Training will start.
A base model will be loaded from latest saved next-generation model. If not existed, BestModel is used.
Trained model will be saved every 2000 steps(mini-batch) after epoch. 

Options:
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)
* `--total-step`: specify total step(mini-batch) numbers. The total step affects learning rate of training. 

```bash
python src/connect4_zero/run.py eval
```

When executed, Evaluation will start.
It evaluates BestModel and the latest next-generation model by playing about 200 games.
If next-generation model wins, it becomes BestModel. 

Options:
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)
* `--single`: run a single loop of evaluation against BestModel, without overwriting.

Model configurations can be set in ```alpha_zero/src/connect4_zero/configs/```.


## References:
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

## Contact

Team members contact:

- Trung Nguyen: trungcn@stanford.edu
- Hormazd Nadir Godrej: hormazd@stanford.edu
- Luke Kim: mkim14@stanford.edu

