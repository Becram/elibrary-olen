# Pustakalaya Project: Continous Integration and Deployment
E-Pustakalaya is an education-focused free and open digital library. It contains thousands of books, educational videos, audio-books, reference materials and interactive learning software.
E-Pustakalaya is accessible on the Internet fron [here](www.pustakalaya.org).
## Technology used:
**Development :** Python's Django Framework, Elatic search, Postgres, Celery, Rabbitmq
**Deployment:** Docker, Docker-swarm, Docker compose, gitlab-ci, Bash

## Archecture:
Pustakalaya is a digital library which is a repositiory for around 8000 pdf, videos and audios. It is developed in Python's Django framework and implements elaticsearch for the lighting search of the content.

We have implemented Docker ro containerise the deloyment. For development we have docker-compose method and for production we have docker-swarm mode. Docker swarm mode is easy method to deployment with minimum downtime and provisions easy rollback in case of failure.
[image of the architecture]

### Directory structure
[tree images]
All the dockerfiles are located a respective **dockerfile-[xxxx]**. Inside the docker
file-[CONTAINER] folder you may find two main files **Dockerfile.dev** and **Dockerfile.build**. **Dockerfile.dev** is used for development by developers while **Dockerfile.build** will used for production ie to create image  for final deployment. Apart from these two files you will also find repective container's  configuration files and script files and also the Dockerfile of each major relase tag (we will get to it later).

All the developer's code are located in **src** folder. Deveopers are encouraged not to tweak the Dockerfiles unless extremely necessary.







<!--
Pustakalaya
============
.. image:: https://readthedocs.org/projects/pustakalaya/badge/?version=latest
    :target: http://pustakalaya.readthedocs.io/?badge=latest
    :alt: Documentation Status



.. image:: http://www.olenepal.org/wp-content/uploads/2016/08/ole-logo-new-mainpage.png
    :alt: Ole Nepal
    :align: left
    :scale: 70 %


Getting started guide
=======================
Check out our latest pustakalaya `docs <http://pustakalaya.readthedocs.io/install.html>`_ -->
