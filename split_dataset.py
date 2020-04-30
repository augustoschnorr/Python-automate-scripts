#!python
"""
Splits an image dataset which files are contained in one `origin` directory into 3 folders for train, evaluation and
test respectively.
The 3 resultant directories are created inside the `destination` directory.
"""
import math
import os
import argparse
import random
from shutil import copyfile


def infer_dataset_location():
    """
    checks if the current working directory has only only directory. It it does, assume it is the dataset directory.
    :return: the path of the inferred dataset directory
    """
    cwd = os.getcwd()
    not_hidden_directories = next(os.walk(cwd))[1]  # only dirnames from the 3-tuple (dirpath, dirnames, filenames)

    not_hidden_directories = list(filter(lambda item: (not item.startswith('.')), not_hidden_directories))

    if len(not_hidden_directories) > 1:
        raise ValueError('`origin` directory was not provided and could not be inferred.')

    return os.path.join(cwd, not_hidden_directories[0])


if __name__ == "__main__":

    # argument_parser = argparse.ArgumentParser()
    # argument_parser.add_argument("-i", "--origin",
    #                              help="Relative path to the directory where the original images are located",
    #                              default=infer_dataset_location()
    #                              )
    # argument_parser.add_argument("-o", "--output_dir",
    #                              help="Relative path to output directory",
    #                              default=os.getcwd())
    # args = vars(argument_parser.parse_args())
    #
    # cwd = os.getcwd()
    # origin = os.path.join(cwd, args["origin"])
    # output_dir = os.path.join(cwd, args["output_dir"])
    #
    # print('Origin:', origin)
    # print("output_dir:", output_dir)
    #
    # path = infer_dataset_location()

    # Defining paths
    images_origin_path = 'C:\\Users\\Alcsaw\\Google Drive (augustoschnorr@mx2.unisc.br)\\BCCD_Dataset\\BCCD\\JPEGImages'
    annotations_origin_path = 'C:\\Users\\Alcsaw\\Google Drive (augustoschnorr@mx2.unisc.br)\\BCCD_Dataset\\BCCD' \
                              '\\Annotations'
    destination_path = 'C:\\Users\\Alcsaw\\Google Drive (augustoschnorr@mx2.unisc.br)\\BCCD_Dataset\\BCCD\\datasets'
    image_extension = '.jpg'
    annotation_extension = '.xml'

    train_path = os.path.join(destination_path, 'train')
    validation_path = os.path.join(destination_path, 'validation')
    test_path = os.path.join(destination_path, 'test')

    print("\nOrigin:", images_origin_path)
    print("\nDestination:", destination_path)

    # Defining dataset rates
    train_percentage = 0.70
    validation_percentage = 0.2
    test_percentage = 0.1

    # Get the name of each image of the original dataset
    images_names = os.listdir(images_origin_path)
    images_list = []

    for img in images_names:
        images_list.append(img.split('.')[0])

    # Shuffling images to prevent bias
    random.shuffle(images_list)

    # Defining quantities of each subset
    image_quantity = len(images_list)

    # Rounding up so no image is left unused
    train_quantity = math.ceil(train_percentage * image_quantity)
    validation_quantity = math.ceil(validation_percentage * image_quantity)
    test_quantity = math.ceil(test_percentage * image_quantity)

    # Allocating images to each dataset
    train_set = images_list[0:train_quantity]
    validation_set = images_list[train_quantity:(train_quantity + validation_quantity)]
    test_set = images_list[(train_quantity + validation_quantity):]

    # Sorting again just for readability
    train_set = sorted(train_set)
    validation_set = sorted(validation_set)
    test_set = sorted(test_set)

    subsets = [('train', train_set), ('validation', validation_set), ('test', test_set)]

    # writing text files with the names of the images of each subset
    print('\n\nGenerating text files with the names of the images of each subset...\n')
    for subset_name, subset in subsets:
        location = os.path.join(destination_path, subset_name + '.txt')

        with open(location, 'w') as text_file:
            print('Writing to', location)
            for item in subset:
                text_file.write(item + '\n')
    print("Finished writing text files.\n")

    # copying images of the subsets to their respective directories
    print('\n\nCopying images of the subsets to their respective directories...\n')
    for subset_name, subset in subsets:
        image_destination = os.path.join(destination_path, subset_name, 'images')
        annotations_destination = os.path.join(destination_path, subset_name, 'annotations')

        for image in subset:
            image_name = image + image_extension
            img_src_path = os.path.join(images_origin_path, image_name)
            img_dst_path = os.path.join(image_destination, image_name)
            copyfile(img_src_path, img_dst_path)

            annotation_name = image + annotation_extension
            annotation_src_path = os.path.join(annotations_origin_path, annotation_name)
            annotation_dst_path = os.path.join(annotations_destination, annotation_name)
            copyfile(annotation_src_path, annotation_dst_path)

    print("Finished copying images.\n")
