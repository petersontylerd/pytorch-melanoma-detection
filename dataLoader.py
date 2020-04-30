import shutil
import os
from glob import glob

import numpy as np
import pandas as pd

def process_label_df(file):
    # load file into df and set image name as index
    df = pd.read_csv(file)
    df = df.set_index("image")

    # create list of class labels from column header
    classes = df.columns

    # create multiclass and binary class labels, remove original columns
    df["multi"] = ""
    for label in classes:
        df["multi"] = np.where(df[label] == 1, label, df["multi"])
        df = df.drop(label, axis=1)

    df["binary"] = np.where(df["multi"] == "MEL", "MEL", "NONMEL")

    return df

def image_sort(destination_root, image_root, label_df, sort_type="binary"):
    """
    Description
    -------------
    Within the provided root path, create a subdirectory for each value in the list
    passed to dirsToAdd.

    Parameters
    -------------
    destination_root, str
    imageRoot, str
    labelDf, Pandas DataFrame
    sortType, str, "multi" or "binary"
    """
    files = glob(os.path.join(image_root, "*.jpg"))
    print("Total number of images: {}\n".format(len(files)))

    # create destination root if it neede
    if not os.path.exists(destination_root):
        os.mkdir(destination_root)

    for file in files:
        # file name without the image file type
        file_name = os.path.split(file)[1].split(".")[0]

        # get label from dfLabel
        label = label_df.loc[file_name][sort_type]

        # set destination folder based on label if it doesn't exist, make it
        destination = os.path.join(destination_root, label)
        if not os.path.exists(destination):
            os.mkdir(destination)

        # copy file to destination
        shutil.copy2(file, destination)

    # print image counts among subfolder
    for folder in os.listdir(destination_root):
        print("{}: {} images".format(folder, str(len(glob(os.path.join("{}/{}".format(destination_root, folder),"*.jpg"))))))