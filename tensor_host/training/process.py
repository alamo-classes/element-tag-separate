"""
Iterate through the training_old dataset to create dataset folders by Lego Element
Used to sort captured photographs
"""
import os
import shutil
import pandas as pd


def organize_dataset(config_args):
    """
    Given a CSV of labels and a directory of images, correctly sort the images into their respect folders.
    :param config_args: Arguments from the configuration file
    """
    # Set file paths
    artifact_dir = config_args["Artifacts"]["artifact_dir"]
    dataset_path = os.path.join(artifact_dir, 'dataset/')
    train_data = os.path.join(artifact_dir, 'train/')

    # Read the labels CSV
    df = pd.read_csv(os.path.join(artifact_dir, 'labels.csv'))
    files = os.listdir(train_data)
    print("Organizing dataset by creating folders by LEGO element part number")
    for file in files:
        # Define folder name reference in labels csv by 32 UUID file name
        folder_name = df.loc[df['id'] == file.split('.')[0], 'part_num'].values[0]

        # Sort the images in the csv to the corresponding directory
        os.makedirs(os.path.join(dataset_path, str(folder_name)), exist_ok=True)
        source = os.path.join(train_data, file)
        destination = os.path.join(dataset_path, str(folder_name), file)
        shutil.copy(source, destination)

    print("Successfully sorted the training_old data by part number and copied images into respective folders")
