# Shift2Rail - Entity Mapping Project 

Library for Shift2Rail project for performing automatic entity mappings

## Requirements
### Informations
The current software version 0.1.4 is a web application that consists of two docker containers activated through a 
docker-compose file provided with the installation package. 

A backend API container is created exposing a process running on the host machine and listening on port 8080 by default. 
This process represents the core of the application and it is not necessary to expose the port it is using as it is meant 
for internal communications only unless the goal is to create alternative UI to what is provided in the package.

An additional NginX container is orchestrating incoming http requests and acting as a reverse proxy towards the internal 
API process. It expects port 80 to be exposed on the host machine by default. 
This container is secondary to the application usage and it is meant only to facilitate the installation process and can 
be replaced with a custom service that acts as a web server for the application's UI. 
In the latter case the minimal configuration installation should be followed.

### Technical requirements
The application was tested on the following configurations:
 * CentOS/RHEL based Amazon Linux AMI 2018.03 x64
 * 8 vCPUs 2.3 GHz, Intel Broadwell E5-2686v4
 * 32 GB RAM
 * 32 GB internal dick storage
 
Although not necessary to replicate, these configurations allowed the application to be
run asynchronously and in a multi-threaded environment which inherently augmented
the throughput.

The minimal set of requirements are defined as follows:
 * An operative system capable of running docker and compose version 3 or above
 * a multi-core CPU with at least 2GHz  frequency
 * at least 5GB of available storage on the disk
 * at least 8GB of RAM
 
 
## Usage


## Maintainers
Current maintainers:
 * Alireza Javadian - https://github.com/AlirezaJavadian
 * Safia Kalwar - https://github.com/safia-k
 * Alexander Nemirovskiy - https://github.com/alexander-nemirovskiy
 * Mersedeh Sadeghi - https://github.com/mersedehSa
