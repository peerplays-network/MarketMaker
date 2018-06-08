This API interacts with the Peerplays blockchain through RPC calls. The API itself is RESTful.

RUN
To run on the command line, run
python3 bookie-api.py # enter your peerplays wallet password
As this API depends on the python peerplays library, please ensure it is installed with 'pip3 install peerplays --upgrade'

DOCKER
To run a dockerized container, run
docker build -t pbsa/bookie-api:1.0 . #will be obsolete once uploaded to dockerhub
docker-compose up bookie-api

The dockerized container will be pointing to Charlie chain and will have nathan set as the default account.
The API is accessible on 127.0.0.1:5000