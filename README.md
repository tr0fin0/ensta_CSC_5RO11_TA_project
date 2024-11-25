# CSC_5RO11_TA, AI for Robotics Project

## Description

The project wants to create an interactive guessing game with [Pepper Robot](https://us.softbankrobotics.com/pepper) to evaluate user response when tricked. Its structure is presented below:

```
├── api/
│   └── pepperAPI/
│       ├── pynaoqi/
│       ├── main.py
│       └── pepper_api.py
|
├── environments/
│   ├── backend.yml
|   └── pepperapi.yml
|
├── interface/
|   ├── app/
|   |   ├── database/
|   |   │   └── reponses.csv
|   │   ├── __init__.py
|   │   ├── models.py
|   │   ├── routes.py
|   |   └── run.py
|   |
|   ├── assets/
|   │   ├── icons/
|   │   └── images/
|   ├── css/
|   │   └── styles.css
|   ├── js/
|   |   └── script.js
|   |
│   └── index.html
|
├── .gitignore
├── LICENSE
└── README.md
```

[`api/`](./api/) contains a custom Python 2.7 PepperAPI library based on [Aldebaran's Python SDK](https://www.aldebaran.com/en/support/nao-6/downloads-softwares) used for controlling Pepper.

[`app/`](./app/), [`assets/`](./assets/), [`database/`](./database/) and [`templates/`](./templates/) contains Back-End and Front-End files used for the UX/UI of the Guessing Game hosted in GitHub Pages under: https://tr0fin0.github.io/ensta_CSC_5RO11_TA_project/templates/index.html.

[`environments/`](./environments/) contains Miniconda environment required for project.

## Installation

### Requirements

Project was developed in Windows 11 and WSL 2 with Ubuntu under VSCode IDLE. Find below a brief requirements explaination:
- Windows:
  - [VSCode](https://code.visualstudio.com/download), Visual Studio Code: programming IDLE;
  - [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), Windows Subsystem for Linux: allow Ubuntu usage inside Windows;
    - [Git](https://git-scm.com/downloads): distributed version control system;
    - [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/): package management system;
    - [NAOqi](https://www.aldebaran.com/en/support/nao-6/downloads-softwares): Aldebaran's Python API for Pepper;

### Git

As the code was developed in six hands we used [Git](https://git-scm.com/) as our distributed version control system and the project was stored in [GitHub/tr0fin0/ensta_CSC_5RO11_TA_project](https://github.com/tr0fin0/ensta_CSC_5RO11_TA_project).

Open a `bash` terminal in WSL 2 via VSCode then run the following to install Git and clone the project repository:

```bash
sudo apt-get install git-all

git clone https://github.com/tr0fin0/ensta_CSC_5RO11_TA_project CSC_5RO11_TA_project
```

### NAOqi

Download the `SDKs 2.8.7 - Python 2.7 SDK` file as `.tar.gz` from [Aldebaran's Download Softwares](https://www.aldebaran.com/en/support/nao-6/downloads-softwares) site and place it in the `src` folder of the project.

In the `api/pepperapi/` folder of the project, run the following command to extract Aldebaran's Python SDK package files:

```bash
tar -xvzf pynaoqi-python2.7-2.8.7.4-linux64-20210819_141148.tar.gz
```

Then run the following command to add the SDK package to Python's environment path:

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/pynaoqi-python2.7-2.8.7.4-linux64-20210819_141148/lib/python2.7/site-packages
```

### Miniconda

Run the following commands to install Miniconda and create the suitable environments:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

conda env create --file environment.yml
```

#### Activate

Run the following to activate the Miniconda environment:
```bash
conda activate CSC_5RO11_TA_project
```

#### Deactivate

Run the following to deactivate the Miniconda environment:
```bash
conda deactivate
```


### AWS

To download the AWS dependencies required for image recognition, follow the steps suggested in [AWS Tutorial](https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html).

First, to you use Amazon Rekognition, you must complete the following tasks:

1. Create an AWS account and [sign up](https://signin.aws.amazon.com/signup?request_type=register). 
2. Create a User with administrative access.
   a. Enable IAM Identity Center.
   b. In IAM Identity Center, grant administrative access to a user.
   c. Sign in as the user with administrative access using the sign-in URL that was sent to your email. 
3. Download and install the AWS CLI and the [AWS SDKs](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) that you want to use.
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
4. Create an access key for the user you created.
   a. Sign in to the AWS Management Console and open the IAM console.
   b. Choose Users and the name of the user you created.
   c. Choose the Security credentials tab and then create access key.
5. Give the user access to be able to use rekognition
   a. Go to the Users section and select the name of the user you want to assign permissions to.
   b. On the Permissions tab, click Add Permissions.
   c. Select Attach Policies Directly.
   d. Find and select the **AmazonRekognitionFullAccess** predefined policy. This will give them full access to the Rekognition service.
   e. Click Review and then Add Permissions.
 6. On your computer, navigate to your home directory
 ```bash
~/.aws
touch credentials
nano credentials
```

7. Using the credentials created in step 4, change the credentials file settings to as shown below

 ```bash
[default]
aws_access_key_id = your_access_key_id
aws_secret_access_key = your_secret_access_key
```

8. Create the config file to define the location.

 ```bash
touch config
nano config
```

9. It is recommended to use the Ireland location, since it has the rekognition feature enabled, which Paris does not.

 ```bash
[default]
region = your_aws_region
```

10. Close the terminal


# How to use the code

## Pepper API and emotion recognition

To use the code that allows you to recognize emotions and also Pepper's responses, you must use the Ubuntu cmd window.

For this first of all you need to activate the miniconda environment created previously.

```bash
conda activate CSC_5RO11_TA_project
```

Then you must navigate to the location where the Naoqi API is installed, as shown below :

```bash
cd path/to/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages
```

To run the Web.py code it is necessary to indicate the position of python in the virtual environment, and then indicate the path where the program is saved.

```bash
/path/to/miniconda3/envs/CSC_5RO11_TA_project/bin/python /path/to/Web.py
```

**Note**: Inside Web.py, in the main part, change the IP address of the Pepper robot if necessary for a correct connection.

After this, Pepper's camera should turn on and the game will start playing.

When finished, to close and unsubscribe from Pepper's camera, just press "Q". This will also immediately display a pie chart with a summary of the emotions captured by Pepper throughout the session.
 

## Roadmap
This project had incremental goals:
1. k

## Authors and Acknowledment
- [Guilherme TROFINO](mailto:guilherme.trofino@ensta-paris.fr):
  - [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/guilherme-trofino/)
  - [![GitHub](https://i.stack.imgur.com/tskMh.png) GitHub](https://github.com/tr0fin0)
- [Gianluca BAGHINO GOMEZ](mailto:gianluca.baghino@ensta-paris.fr):
  - [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn]()
  - [![GitHub](https://i.stack.imgur.com/tskMh.png) GitHub](https://github.com/gianlucabaghino)
- [Natalia GALLEGO](mailto:natalia.gallego@ensta-paris.fr):
  - [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/natalia-gallego-castrillon-825a4b208/)
  - [![GitHub](https://i.stack.imgur.com/tskMh.png) GitHub](https://github.com/NataliaGCR)

We greatly appreciate our CSC_5RO11_TA teachers at [ENSTA](https://www.ensta-paris.fr/):
- [Adriana TAPUS](mailto:adriana.tapus@ensta-paris.fr)
- [Adnan SAOOD](mailto:adnan.saood@ensta-paris.fr)
- [Juan Jose GARCIA CARDENAS](mailto:juan-jose.garcia@ensta-paris.fr)
