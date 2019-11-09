import os.path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

if __name__ == '__main__':
    if os.path.isdir("data") and os.path.isfile("data/connect-4.dat"):
        print("Data has already been downloaded.")
    else:
        print("Downloading data...")

        # For data description, see
        url = "https://sci2s.ugr.es/keel/dataset/data/classification/connect-4.zip"
        resp = urlopen(url)
        with ZipFile(BytesIO(resp.read())) as zipfile:
            zipfile.extractall("data")

        # Cleaning the data format
        with open("data/connect-4.dat", "r") as f:
            lines = [line for line in f if line[0] is not "@"]

        with open("data/connect-4.dat", "w") as f:
            f.writelines(line.replace("win", "1")
                         .replace("loss", "-1")
                         .replace("draw", "0") for line in lines)

        print("Finished downloading data")
