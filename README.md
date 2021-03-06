# Anonymization Tool
An open-source Dataset Anonymization Tool

# How to Run Our Tool
### 1. Docker Compose Installation
NOTE: Docker must be installed on your computer/server for this tool.    
Docker Installation Instructions: [here](https://docs.docker.com/engine/installation/).  

*Operating Systems    
1. If you are a Mac or Windows user:  
You are done! Docker compose in already installed along with your docker.  
2. If you are a Linux user:  
Docker-compose Installation Instruction: [here](https://docs.docker.com/compose/install/). (Only for Linux User)  

### 2. Launch Our Tool
1. Make sure you have docker-compose installed
2. Download the code from our github repository 
3. Go the the directory with `docker-compose.yml`, run `docker-compose up`  
Note that the initial attempt of running this command will take several minutes to build the image. After the first build, it will be faster.
4. Visit our tool at `localhost:8000` with your browser.

# Repository Directory
```
├── Dockerfile          # Docker configuration file.
├── LICENSE.txt         # License
├── README.md           # README File
├── app                 # Flask App Folder
│   └── code            
│       ├── boot.sh             # boot script of backend container
│       ├── db.py               # Database interfaces
│       ├── flaskapp_uwsgi.ini  # uwsgi Configure for Flask 
│       ├── log                 # Backend Logs Folder
│       ├── server.py           # Flask Backend web server
│       └── templates           # Frontend Files
├── config              # Configuration folder
│   ├── eps.conf                # Configuration file for nginx
│   └── requirements.txt        # Python Requirements file  
├── dataset         # Folder to put csv dataset
├── docker-compose.yml      # Docker compose configuration file
└── robots.txt      # Robot rule



```
