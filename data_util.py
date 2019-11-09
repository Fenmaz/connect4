import os.path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

if __name__ == '__main__':
    if os.path.isdir("data") and os.path.isfile("data/connect-4.data"):
        print("Data has already been downloaded.")
    else:
        print("Downloading data...")

        # For data description, see
        url = "https://drive.google.com/uc?export=download&id=1B3wRs75_mFrSZbAJQFIZIxt6G1jTKMzm"
        resp = urlopen(url)
        with ZipFile(BytesIO(resp.read())) as zipfile:
            zipfile.extractall("data")

        print("Finished downloading data")
