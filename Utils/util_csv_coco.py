# util.py
import os
import json
import pandas as pd

from PIL import Image
from sys import exit, argv
from tqdm import tqdm

if len(argv) != 3:
    print("Usage: python util.py -t|v labels.csv")
    exit(1)

if argv[1] != '-t' and argv[1] != '-v':
    print("Please use -t (train) or -v (val) flag.")
    exit(1)

# DIRECTORIES
ROOT_DIR = os.getcwd()
PROJECT_DIR = os.path.join(ROOT_DIR, 'brownspot')
TRAIN_DIR = os.path.join(PROJECT_DIR, 'train')
VAL_DIR = os.path.join(PROJECT_DIR, 'val')
ANNOTATIONS_DIR = os.path.join(PROJECT_DIR, 'annotations')

ANNOTATION_FILE = argv[2]
ANNOTATION_PATH = os.path.join(ROOT_DIR, ANNOTATION_FILE)
CUR_DIR = TRAIN_DIR if argv[1] == '-t' else VAL_DIR

# print(PROJECT_DIR, TRAIN_DIR, VAL_DIR, ANNOTATIONS_DIR, ANNOTATION_PATH, sep="\n")

def main():
    # Make directories
    DIRS = [TRAIN_DIR, VAL_DIR, ANNOTATIONS_DIR]
    make_dirs(DIRS)

    # COCO format file
    FLAG = "train" if argv[1] == '-t' else "val"
    OUTPUT_ANNOTATION_FILE = os.path.join(ANNOTATIONS_DIR, "instances_" + FLAG + ".json")
    LABELS = pd.read_csv(ANNOTATION_PATH)

    # make and create coco file
    COCO_DATA = make_coco_file(LABELS)
    create_file(COCO_DATA, OUTPUT_ANNOTATION_FILE)

def make_dirs(dirs):
    """Creates directories that don't already exist."""
    for dir in dirs:
        if not os.path.isdir(dir):
            os.mkdir(dir)

def make_coco_file(labels):
    """Creates a COCO format data structure."""

    columns = labels.columns
    # COCO ANNOTATION FORMAT
    categories = ['brownspot']
    annotation_list = []
    foo = {}
    foo["supercategory"] = "master"
    foo["id"] = 0
    foo["name"] = categories[0]
    annotation_list.append(foo)

    # Might need to create a YML
    COCO_DATA = {}
    COCO_DATA["type"] = "instances"
    COCO_DATA["images"] = []
    COCO_DATA["annotations"] = []
    COCO_DATA["categories"] = annotation_list

    image_id = 0 # Image id
    annotation_id = 0 # Annotation id

    i = 0
    length = len(labels)

    # Follow on the progress
    pbar = tqdm(total=length, desc="Working")
    while (i < length):
        file_name = labels[columns[0]][i]
        image_path = os.path.join(CUR_DIR, file_name)

        if (not os.path.isfile(image_path)):
            continue
        image = Image.open(image_path)
        width, height = image.size

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

            anno = {}
            anno["id"] = annotation_id
            annotation_id += 1
            anno["image_id"] = image_id
            anno["segmentation"] = []
            anno["ignore"] = 0
            anno["area"] = (xmax - xmin) * (ymax - ymin)
            anno["iscrowd"] = 0
            anno["bbox"] = [xmin, ymin, xmax - xmin, ymax - ymin]
            anno["category_id"] = 0 # There is only one class

            COCO_DATA["annotations"].append(anno)

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
