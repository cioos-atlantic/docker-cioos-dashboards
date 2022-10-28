# Dockerized version of the CIOOS Dashboard Visualizations

To begin:

- Clone the repo:

`git clone https://github.com/cioos-atlantic/docker-cioos-dashboards`
`cd docker-cioos-dashboards`

- Build the docker file:

`docker build -t dashboard .`

- Run the docker container in the desired port (include a -d to run in detached mode):

`docker run -p 8050:8050 .`