from classification.src.data_util import fetch_train_val
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import numpy as np

PIECE = {b"b": 0, b"x": 1, b"o": -1}
OUTCOME = {b"loss": 0, b"draw": 1, b"win": 2}


def main():
    x_train, y_train, x_dev, y_dev = fetch_train_val(x_converter_func=PIECE.get, y_converter_func=OUTCOME.get)

    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class="multinomial",
                             max_iter=1000, verbose=False)
    clf.fit(x_train, y_train)
    train_accuracy = clf.score(x_train, y_train)
    accuracy = clf.score(x_dev, y_dev)
    y_pred = clf.predict(x_dev)

    confusion_mat = confusion_matrix(y_dev, y_pred)

    # Print metrics on inputs and outputs
    print("The order of classes are: loss, draw, win")

    print("Train set classes counts: {}".format(np.unique(y_train, return_counts=True)[1]))
    print("Dev set classes counts: {}".format(np.unique(y_dev, return_counts=True)[1]))

    print("Accuracy on train set is {}".format(train_accuracy))
    print("Accuracy on dev set is {}".format(accuracy))
    print("Confusion matrix is (in sorted order) \n{}".format(confusion_mat))


if __name__ == '__main__':
    main()
