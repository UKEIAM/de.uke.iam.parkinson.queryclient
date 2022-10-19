# Overview

This repository contains the Queryclient for the project [Parkinson Algorithm deTecT movEment patteRNs](https://www.uke.de/organisationsstruktur/zentrale-bereiche/apotheke/3d-druck-von-arzneimitteln/index.html). The Queryclient accepts print jobs, stores them in a database and allows the processing/acceptance/deletion of jobs via a GUI by a user. Print jobs can be send to a REST-API, that interacts with a [PostgreSQL database](https://www.postgresql.org/) storing the print jobs. The frontend is a [Node.js server](https://nodejs.org/en/), where the user can accept or delete open jobs. The 3D medication printer is handled by the [Repetier software](https://www.repetier.com/). The QueryClient uses [Docker](https://www.docker.com) to create three seperate containers for safety and reproducibility. The frontend can be accessed through the browser of your choice, e.g. [Firefox](https://www.mozilla.org/de/firefox/new/).

# Installation/Quickstart

* Install Docker from [here](https://www.docker.com/)
* Clone or download this repository
* Call `docker-compose up --build` in the terminal (Powershell on Windows)
* Wait until all four containers where started, you can track their status with `docker container ls` or in the desktop app
* Open the user interface of the QueryClient in your browser under [localhost:50604](http://localhost:50604)

# Sending print jobs to the REST-API

You can send print jobs with a POST request using the JSON format. From the shell this can be done with a command like `curl -X POST -H "Content-Type: application/json" -d '{"dataString" : "Mustermann|Max|1990-12-25|0815|Station 1|MedPrint3D|Med 100 mg|1.5|2022-09-09 15:21"}' -i localhost:50602/incoming`. In the Powershell the corresponding command would be `curl.exe -X POST -H "Content-Type: application/json" -d '{\"dataString\" : \"Mustermann|Max|1990-12-25|0815|Station 1|MedPrint3D|Med 100 mg|1.5|2022-09-09 15:21\"}' -i localhost:50602/incoming`

# Install label printer

In this section we assume that you use a Linux distribution.

* Plug the label printer in an USB port
* Install CUPS (if not existing) with `sudo apt install cups cups-client`
* Check the adress of the printer with `sudo lpinfo -v`
* If e.g. the adress is `usb://TSC/TDP-225?serial=000001`, add the printer with `sudo lpadmin -p labelprinter -v usb://TSC/TDP-225?serial=000001`. Here it is important, that you name the printer "labelprinter"
* Enable the printer with `sudo cupsenable labelprinter`
* Let it accept print jobs with `sudo cupsaccept labelprinter`

# Access medication printer

* Plug the medication printer in the Ethernet port
* Access rights of your computer might have to be configured on the medication printer
* You can open the Repetier frontend of the printer [here](http://192.168.2.100:3344)
* In the frontend, go to "Global Settings" and then "Connectivity". Copy the current API key and insert it for the variable `REPETIER_API_KEY` as a string
* If not already existing, upload all relevant G-Code files for the printer and name them with the corresponding logistics ID from IDMedics

# Add frontend to startup

For this configuration we assume that you use a Linux distribution and `cron` and [Firefox](https://www.mozilla.org/de/firefox/new/) are installed

* Open the shell and type `crontab -e`
* Select an editor, we recommend `nano` or `vim`
* Add the line `@reboot /usr/bin/firefox http://localhost:50604`
