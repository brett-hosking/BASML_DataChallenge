# BASML_DataChallenge
Classification of Benthic Megafauna in Images

## Install and setup virtualenv:

### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Create virtualenv using Python3
    virtualenv -p python3 basml

### Instead of using virtualenv you can use this command in Python3
    python3 -m venv basml

## Activate virtual environment

### Unix

    source basml/bin/activate

### Windows 

    basml/Scripts/activate
    
>the environment can be deactivated with the **deactivate** command


# Make sure all of the libraries you need are installed
    
    pip install -r requirements.txt