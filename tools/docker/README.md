# TobaccoFeed Docker deployment

## Content of working folder

Working folder must contain:

* Dockerfile
* private.py module from TobaccoFeed
* start_tf.sh script

### Content description

* Dockerfile

Contains all info about configuration order (build and deploy)

* private.py

The part of TobaccoFeed web server. Contains secret passwords ant etc

*Note: this file can't be found on Git*

* start_tf.sh

Script udpates and runs server with parsed container IP and port

## Building image

Container is based on Ubuntu.
You can pull ubuntu by hands: `docker pull ubuntu`
Then launch terminal and go to folder with Dockerfile and scripts

`docker build -t tf_ubuntu .`

Wait for a long time (~10 min) if it's your first build.
Container will be updated, upgraded, equiped with git, python and other modules.

## Running container

As soon as scripts are launching server on port 8000 we must forward it in docker `run` command

`docker run -p 8000:8000 -it tf_ubuntu`

Enjoy :)