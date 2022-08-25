# Overview
This repository contains the Queryclient for the project [Parkinson Algorithm deTecT movEment patteRNs](https://www.uke.de/organisationsstruktur/zentrale-bereiche/apotheke/3d-druck-von-arzneimitteln/index.html). The Queryclient accepts print jobs, stores them in a database and allows the processing/acceptance/deletion of jobs via a GUI by a user. Print jobs can be send to a REST-API, that interacts with a [PostgreSQL database](https://www.postgresql.org/)  storing the print jobs. The frontend is a [Node.js server](https://nodejs.org/en/), where the user can accept or delete open jobs. The QueryClient uses [Docker](https://www.docker.com) to create three seperate containers for safety and reproducibility.

# Installation/Quickstart

- Install docker-compose from [here](https://github.com/docker/compose/releases)

- Clone repository

- Call ```docker-compose up```

- Wait until all three containers where started

- Open frontend in browser under [localhost:50604](http://localhost:50604)

# Remote deployment

When working with a remote docker host (like in the IAM group), you need to adjust the above workflow
## On the docker host
- Clone repository

- Call ```docker-compose up```
## On your local machine
- start tunnel to the REST-API with
```ssh <username>@docker -L 50602:localhost:50602 -J jumper@stargate.fordo.de:56023```
- start tunnel to node.js-Server with
```ssh <username>@docker -L 50604:localhost:50604 -J jumper@stargate.fordo.de:56023```
- Open frontend in browser under [localhost:50604](http://localhost:50604)

# Sending print jobs to the REST-API
You can send print jobs with a POST request using the JSON format. From the shell this can be done with a command like
```curl -X POST -H "Content-Type: application/json" -d '{"surname" : "ImGlueck", "givenName":"Hans", "birthday":"1990-12-24", "logisticsID":122, "medicationName":"Ibuprofen", "medicationDose":"70/30", "medicationUnit":"mg", "medicationTimestamp":"2022-01-01 15:22:15", "hospitalWard":"Station 1"}' -i localhost:50602/incoming```

# TODOs

- Adjust paths in ```docker-compose.yml``` and ```Dockerfile_api``` for production
- Add interaction with 3D printer
- Add interaction with label printer
- Maybe adjust ports for convenience
- Delete processed jobs
- Remove seconds from dose timestamp
- Refresh table on frontend every couple seconds
- Maybe additional refresh button
- add script/bash_rc config to open frontend on restart
- add documentation to code
