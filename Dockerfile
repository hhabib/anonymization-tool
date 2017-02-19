# Docker image build file for EPS anonymization tool Project
# Note that this is for a development environment docker
# Docker version V0.1

# Ubuntu Linux as the base image
FROM ubuntu:16.04

# Update the repository
RUN apt-get update

# Install necessary tools
#RUN apt-get install -y tar git curl vim wget dialog net-tools 
RUN apt-get install -y vim curl

# Download and Install Nginx
RUN apt-get install -y nginx  

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/sites-enabled/*

# Copy a configuration file from the current directory
ADD ./config/eps.conf /etc/nginx/sites-enabled/eps.conf

# Copy frontend files
# In final version, we will do copy, but in dev, we use -v
# ADD ./frontend /var/www/eps/

# Start nginx
RUN service nginx restart

# Install Python and Basic Python Tools
RUN apt-get install -y build-essential python python-dev python-distribute python-pip
RUN pip install --upgrade pip 

# Add the files
#ADD ./config/requirements.txt /
#RUN pip install -r requirements.txt

# Copy backend files
# In final version, we will do copy, but in dev, we use -v
#ADD ./backend/code /code

# Define the command which runs when the container starts
CMD ["service nginx start"]