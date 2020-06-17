# util.py
"""

This script converts a labels.csv file to a COCO format JSON file.
The labels.csv file is expected to be in the following column format:

| 'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax' |

The output file is named instances_(train|val).json depending on the flag
given.

The scripts expects the following file format:
project_name
    - train         (Contains the training images.)
    - val           (Contains the validation images )
    - annotations   (The folder in which the annotations file created is saved)

"""

import os
import json
import pandas as pd

from PIL import Image
from sys import exit, argv
from tqdm import tqdm

if len(argv) != 3:
    print("Usage: python util_csv_coco.py -train|test|val labels.csv")
    exit(1)

if argv[1] != '-train' and argv[1] != '-val' and argv[1] != '-test':
    print("Please use (-train) or (-val) or (-test) flag.")
    exit(1)

FLAG = str(argv[1][1:])

# DIRECTORIES
PROJECT_DIR = os.getcwd() #  project_name: brownspot
TRAIN_DIR = os.path.join(PROJECT_DIR, 'train')
VAL_DIR = os.path.join(PROJECT_DIR, 'val')
TEST_DIR =os.path.join(PROJECT_DIR, 'test')
ANNOTATIONS_DIR = os.path.join(PROJECT_DIR, 'annotations')

ANNOTATION_FILE = argv[2]
ANNOTATION_PATH = os.path.join(PROJECT_DIR, ANNOTATION_FILE)
CUR_DIR = os.path.join(PROJECT_DIR, FLAG)

def main():
    # Make directories and if necessary move the images in the respective folders.
    dirs = [TRAIN_DIR, VAL_DIR, ANNOTATIONS_DIR]
    make_dirs(dirs)

    # COCO format file
    output_annotation_file = os.path.join(ANNOTATIONS_DIR, "instances_" + FLAG + ".json")
    labels = pd.read_csv(ANNOTATION_PATH)

    # Get the category list
    # categories = input("Enter categories separated by space: ")
    # categories = categories.rstrip('\n').lower().split(" ")

    categories = ['brownspot']
    # make and create coco file
    coco_data = make_coco_file(labels, categories)
    create_file(coco_data, output_annotation_file)

def make_dirs(dirs):
    """Creates directories that don't already exist."""
    for dir in dirs:
        if not os.path.isdir(dir):
            os.mkdir(dir)

def make_coco_file(labels, categories):
    """Creates a COCO format data structure."""

    columns = labels.columns

    classes = sorted(categories)
    category_list = []
    # COCO ANNOTATION FORMAT
    for i, category in enumerate(classes):
        foo = {}
        foo["supercategory"] = "None"
        foo["id"] = i + 1 # COCO is one-indexed
        foo["name"] = category
        category_list.append(foo)


    # Might need to create a YML
    COCO_DATA = {}
    COCO_DATA["type"] = "instances"
    COCO_DATA["images"] = []
    COCO_DATA["annotations"] = []
    COCO_DATA["categories"] = category_list

    image_id = 0 # Image id
    annotation_id = 0 # Annotation id

    i = 0
    length = len(labels)

    # Follow on the progress
    pbar = tqdm(total=length, desc="Working")
    while (i < length):
        file_name = labels[columns[0]][i]

        image_path = os.path.join(CUR_DIR, file_name)
        label = str(labels[columns[3]][i])
        #
        if (not os.path.isfile(image_path)):
            continue
        image = Image.open(image_path)
        width, height = image.size

        # width = int(labels[columns[1]][i])
        # height = int(labels[columns[2]][i])

        temp = {}
        temp["file_name"] = file_name
        temp["height"] = height
        temp["width"]  = width
        temp["id"]  = image_id
        COCO_DATA["images"].append(temp)

        # Assign all annotations of a given image once
        while True:
            xmin = int(labels[columns[4]][i])
            ymin = int(labels[columns[5]][i])
            xmax = int(labels[columns[6]][i])
            ymax = int(labels[columns[7]][i])

            temp = {}
            temp["id"] = annotation_id
            annotation_id += 1
            temp["image_id"] = image_id
            temp["segmentation"] = []
            temp["ignore"] = 0
            temp["area"] = (xmax - xmin) * (ymax - ymin)
            temp["iscrowd"] = 0
            temp["bbox"] = [xmin, ymin, xmax - xmin, ymax - ymin]
            temp["category_id"] = classes.index(label) + 1 # There is only one class

            COCO_DATA["annotations"].append(temp)

            # Update i and prevent out of range error
            i += 1
            pbar.update(1)
            if (i >= length):
                break

            next_file = labels[columns[0]][i]

            # Check if next file is the same as the current one.
            if (file_name != next_file):
                break

        # Update image_id
        image_id += 1
    pbar.close() # Progress bar
    return COCO_DATA

def create_file(coco_data, output_file):
    """Create JSON file of the COCO_DATA."""
    f = open(output_file, 'w')
    json_str = json.dumps(coco_data, indent=4)
    f.write(json_str)
    f.close()

if __name__ == '__main__':
    main()
