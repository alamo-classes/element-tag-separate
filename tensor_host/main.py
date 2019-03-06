"""
Python script to capture images, train the Element ID neural network, and then identify elements using the network

Arguments:
-- mode: Choose from one of the following modes:
    1. Setup - Used to write a new configuation file for the LEGO element sorter
    2. Capture - Capture new pictures for a dedicated label. Save pictures and append to the CSV file
    3. Training - Using the label CSV and the training images produce a new neural network through transfer learning
    4. Identify - Using the trained neural network, identify the targeted LEGO element
-- config_pwd: Directory which the configuration file is located
-- label: Label to be set when capturing training data
"""
import argparse
import configparser
import os


def parse_config(config_dir):
    configuration = configparser.ConfigParser()
    if not os.path.exists("{}/config.ini".format(config_dir)):
        print("Configuration file was not found. Please enter the directory where the configuation file is located.")
        print(config_dir)
        exit(0)
    configuration.read("{}/config.ini".format(config_dir))
    return configuration


def setup_config(config_dir):
    """
    Prompt user to create the configuration files for the element sorter
    :param config_dir: The directory to place the configuration directory
    :return: None
    """

    # Prompt user for the directory to place the artifact directory
    artifact_dir = input("Please enter the directory to place the artifact directory [{}]: ".format(
        os.getcwd()))
    if not artifact_dir:
        artifact_dir = os.getcwd()

    # Construct the parser for the user arguments
    configuration = configparser.ConfigParser()

    # Add the artifacts directory to the configuration file
    configuration['Artifacts'] = dict()
    configuration['Artifacts']['artifact_dir'] = artifact_dir

    # Prompt the user to enter the number of Raspberry Pi's that are used in this configuration
    number_of_cams = int(input("Please enter the number of Raspberry Pi's that are used: "))
    configuration['Raspberry_IP']['Number_of_Pies'] = number_of_cams
    pi_ip = dict()
    for pi_num in range(number_of_cams):
        pi_ip[pi_num] = input("Please enter the IP address for Raspberry Pi #{}: ".format(pi_num))
        configuration['Raspbery_IP'][pi_num] = pi_ip

    # Write the configuation file
    with open('{}/config.ini'.format(config_dir), 'w') as configfile:
        configuration.write(configfile)
    print("Configuration file written to \"{}/config.ini\". Exiting...".format(config_dir))


if __name__ == "__main__":
    # Get arguments, if arguments not found then
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode',
        type=str,
        default='identify',
        help="Mode to run. Options: [capture, train, identify, setup]"
    )
    parser.add_argument(
        '--config_pwd',
        type=str,
        default=os.getcwd(),
        help="Path to the configuration file"
    )

    parser.add_argument(
        '--label',
        type=str,
        default="",
        help="Label to be set when capturing images (Mode: Capture)"
    )

    FLAGS, unparsed = parser.parse_known_args()

    # If not already created, generate an artifacts directory
    os.makedirs("{}/artifacts".format(os.getcwd()), exist_ok=True)

    # Setup the configuration file
    if FLAGS.mode == "setup":
        setup_config(FLAGS.config_pwd)

    # Run capture routine
    if FLAGS.mode == "capture":
        config = parse_config(FLAGS.config_pwd)

        print(config["Artifacts"]["artifact_dir"])

    # Run training routine
    if FLAGS.mode == "training":
        config = parse_config(FLAGS.config_pwd)

    # Run identification routine
    if FLAGS.mode == "identify":
        config = parse_config(FLAGS.config_pwd)
