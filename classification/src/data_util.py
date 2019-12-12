import os.path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import numpy as np
from sklearn.model_selection import train_test_split

SEED = 229
D = 42


def fetch_train_val(x_converter_func=None, y_converter_func=None):
    download()
    split(SEED)
    x_converter = {i: x_converter_func for i in range(D)}
    y_converter = {0: lambda s: y_converter_func(s.strip())}
    return (np.loadtxt("data/x_train.data", delimiter=",", converters=x_converter),
            np.loadtxt("data/y_train.data", converters=y_converter),
            np.loadtxt("data/x_dev.data", delimiter=",", converters=x_converter),
            np.loadtxt("data/y_dev.data", converters=y_converter))


def split(seed=None):
    if os.path.isfile("data/x_train.data") and os.path.isfile("data/y_train.data") \
            and os.path.isfile("data/x_dev.data") and os.path.isfile("data/y_dev.data") \
            and os.path.isfile("data/x_test.data") and os.path.isfile("data/y_test.data"):
        print("Data has already been split.")

    elif not os.path.isfile("data/connect-4.data"):
        print("Data has not been downloaded. Please download data first.")

    else:
        data = np.loadtxt("data/connect-4.data", delimiter=",", dtype=str)
        x, y = data[:, :-1], data[:, -1]
        x, x_test, y, y_test = train_test_split(x, y, random_state=seed)
        x_train, x_dev, y_train, y_dev = train_test_split(x, y, random_state=seed)

        save_files = [(x_train, "x_train.data"), (y_train, "y_train.data"),
                      (x_dev, "x_dev.data"), (y_dev, "y_dev.data"),
                      (x_test, "x_test.data"), (y_test, "y_test.data")]

        for data, filename in save_files:
            np.savetxt("data/{}".format(filename), data, delimiter=",", fmt="%s")


def download():
    if os.path.isfile("data/connect-4.data"):
        print("Data has already been downloaded.")
    else:
        print("Downloading data...")

        # For data description, see
        url = "https://drive.google.com/uc?export=download&id=1B3wRs75_mFrSZbAJQFIZIxt6G1jTKMzm"
        resp = urlopen(url)
        with ZipFile(BytesIO(resp.read())) as zipfile:
            zipfile.extractall("data")

        print("Finished downloading data")


if __name__ == '__main__':
    download()
    split(SEED)
