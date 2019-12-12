# Connect 4
> Trung Nguyen, Hormazd Nadir Godrej and Luke Kim

Class project for CS 229: Machine Learning at Stanford University.

Each directory is a separate package for a task with the Connect 4 game.
* ```play```: play a game of Connect 4 on the terminal 
against yourself (or your friend). It serves as a good starting
point for familiarizing oneself with the game.
* ```classification```: given a board position, predict who will be the winner.
The dataset in use is the UIC and the Kaggle dataset. 
** TODO: add hyperlinks to the datasets **
* ```solver```: solve the game using the Minimax algorithm.
* ```alpha_zero```: solve the game using the AlphaZero algorithms. 
More details below.

---

## Requirements
Each packages have a different set of requirements, but they all require 
Python 3.

1. ```play```: None

2. ```classification```: Requires ```scikit``` and ```pygame```
```shell script
pip install scikit pygame
```

3. ```solver```: Requires ```pygame```
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

## References:
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

## Contact

Team members contact:

- Trung Nguyen: trungcn@stanford.edu
- Hormazd Nadir Godrej: hormazd@stanford.edu
- Luke Kim: mkim14@stanford.edu

