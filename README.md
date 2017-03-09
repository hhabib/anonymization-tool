# Anonymization Tool
An open-source Dataset Anonymization Tool

# How to Run Our Tool
### 1. Docker Compose Installation
Docker is required for this tool.    
Docker Installation Instructions: [here](https://docs.docker.com/engine/installation/).  


*Operating Systems:  
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
├── Dockerfile           # Docker configuration file.
├── backend				 # Backend Folder
│   └── code					# Backend code folder
│       ├── boot.sh						# boot script of backend container
│       ├── db.py		 				# Database interfaces
│       ├── flaskapp_uwsgi.ini		    # uwsgi Configure for Flask 
│       ├── log			 				# Backend Logs Folder
│       └── server.py 					# Flask Backend web server
├── dataset				 # Folder to put csv dataset
├── config				 # Configuration folder
│   ├── eps.conf						# Configuration file for nginx
│   └── requirements.txt  				# Python Requirements file  
├── docker-compose.yml   # Docker compose configuration file
├── frontend			 # Frontend Folder
│   ├── 404.html
│   ├── apple-touch-icon.png
│   ├── browserconfig.xml
│   ├── crossdomain.xml
│   ├── css
│   ├── doc
│   ├── favicon.ico
│   ├── humans.txt
│   ├── img
│   ├── import.html
│   ├── index.html
│   ├── js
│   │   ├── main.js
│   │   ├── plugins.js
│   │   └── vendor
│   │       ├── jquery-1.12.0.min.js
│   │       └── modernizr-2.8.3.min.js
│   ├── tile-wide.png
│   ├── tile.png
│   └── tutorials.html
└── robots.txt
```
