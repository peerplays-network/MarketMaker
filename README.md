This API interacts with the Peerplays blockchain through RPC calls. The API itself is RESTful.

RUN
To run on the command line, run
python3 bookie-api.py # enter your peerplays wallet password
As this API depends on the python peerplays library, please ensure it is installed with 'pip3 install peerplays --upgrade'

DOCKER
To run a dockerized container, first edit the Dockerfile with you pertinent connection information, then run
docker build -t pbsa/bookie-api:1.0 . 
docker-compose up -d

The dockerized container will be pointing to chain and using the account from config.yaml
The API is accessible on 127.0.0.1:5000 by default
