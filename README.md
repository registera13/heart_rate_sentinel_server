# heart_rate_sentinel_server
[![Build Status](https://travis-ci.com/registera13/heart_rate_sentinel_server.svg?branch=master)](https://travis-ci.com/registera13/heart_rate_sentinel_server)
Created by Alan Register (azr3) for BME 590 server assignment 

## SERVER USAGE
a ubuntu vm to run this flask server was created on vcm-7319.vm.duke.edu

Server address is https://vcm-7319.vm.duke.edu/. To check if the server is running please input this address in 
your web browser: https://vcm-7319.vm.duke.edu/hello.

If the server is working then you can proceed to api POST and GET request. 

## LOCAL USERGUIDE
requirement pip install are located in requirements.txt and should be installed first in your virtual environment.

"main" flask server is a file called: HRSentinelServer.py this is the file you need to run flask on the local machine.
This is linked to another file called: HRfunction.py, which contain a list of functions that is used for this server.

## Features
*  sSl for https:// are implemented at server side
*  Mlab database was used to store patients information

## DOC Website
https://registera13.github.io/heart_rate_sentinel_server/

 
