# exchange_rate_lambda

* This repo contain api for europass exchange rates using lambda functions, serverless (IaC), DynamoDB and deployed using LocalStack.

Goal of this application is to expose two api:

1. For fetching latest exchange rates.
2. For comparing current exchange rates with respect to previous day.
   To fetch the exchange rates we are using
   https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html


# Architecture:

* To implement above scanario we are using these technologies

1. Python (requests, xml)
2. Serverless as IaC
3. Lambda Functions
4. DynamoDB

* Serverless framework will deploy the this app on the AWS, for local development
we are using localstack (https://localstack.cloud/)
* Lambda functions are implemented using python, for caching the exchange rates, using DynamoDB
* Requests is the only python external library which is also manage by serverless-python-requirements plugin.
* serverless-localstack is also used in serverless to deploy to the localstack instead of AWS


# Setup
* To setup this application first clone this repo.
* These are the environment variables you may need to setup

1.AWS Region (serverless.yml)
2.DYNAMODB_TABLE (serverless.yml)
3.AWS_ACCOUNT_ID and AWS_SECRET needs to be available in
environment.
4. stage (serverless) if you are planning to deploy on someother environments.
After setting up the environment variable next thing is installtion following


### Pyenv
-Using python3.8 for developing this application, its good
idea to use pyenv as swtiching between different python makes it easy. Also if you are on Linux messing with pre-install python is not a good idea.
-Follow this guid https://github.com/pyenv/pyenv to install for your distrubution.


### VirtualEnv for python

* After getting pyenv install python3.8 by typing following in terminal:

`pyenv install 3.8`

and to set local version of python use:

`pyenv local 3.8`

* Recommended way to proceeding with python dependenciues is virutalenv, but you can skip this step


#### VirtualEnv (Can Skip)

* To install virtualenv with your local version of python set by pyenv follow this:

https://pypi.org/project/virtualenv/

* or just type in terminal, before that make sure you in your
directory where you cloned this repo. It should be 'exchange_rate_lambda'

`pip3 install virtualenv`

After successfull installtion type this in terminal:

`virtualenv venv`

* 'venv' is envrionment name where package related to python will be installed. Try to keep this name because it is already included in .gitignore otherwise use anyother name you find suitable and make sure to include it in .gitignore.

* After creating the virtual envrionment time to
active this environments type this in terminal:

`source venv/bin/activate`

* This will activate the virtualenv and you should see '(venv)' placeholder at start of terminal showing that venv is activated for this terminal session.



### Local Python Requirments Installtion

* Now we have our python3.8 and virtual envrionment on top of that time to install dependencies which will be helping us.

* Make sure your in root directory of this repo 'exchange_rate_lambda', this is where the requirments-local.txt file lives.

`pip3 install -r requirments-local.txt`

* This will install everything including LocalStack python. Make sure you ran this command after activating the virtualenv if you planned to use that.



### Local Stack

* In previous step where we install our local python requirments, we already insatalled localstack with it.

* To start first we need docker installed on your system. To do that easiest way is docker desktop to install that follow this guid https://www.docker.com/products/docker-desktop/

* After installation of docker and activating the virtualenv run this command

`localstack start`

* This will take sometime, on first run, because it will be downloading the docker images for localstack. After success run you will see some logs. A very detailed guid is here if you having trouble installing localstack.
https://docs.localstack.cloud/getting-started/installation/



### Installing Serverless and Plugin

* Now we have localstack running on system, we need to install serverless and some plugins. Serverss is node module and it will be installed using npm which is a node package manager just like pip for python. To install everything related to this repo run this command, make sure you are in root of this repo.

`npm install`

* This will load the package-lock.json file and install the everything according to right version. If having trouble you can also follow this guid:
https://docs.npmjs.com/cli/v8/commands/npm-install

* If you need more information of serverless and its plugins you can refer these links:
https://www.serverless.com/plugins/serverless-localstack -https://www.npmjs.com/package/serverless-python-requirements -https://www.serverless.com/plugins/serverless-python-requirements

* Sometime just using 'npm install' will not do the job.
In that case you can install node modules globally with this command:

`npm install -g serverless`
and similar for plugin use links for guidance.


# Pytest

* Before deploying it is always a good idea to have some unit test cases. You can find all the test cases in tests/ directory. To run test in virtualenv type this command

`pytest tests/`

* This will run all the test cases and you will failed if any.

Note: Pytest is not included in deployments as lambad functions have limited space so try to avoid any extra library. We will discuss more how to install python dependencies using serverless plugins.


# Lambda Functions Dependencies/Deployment:

* All the dependencies related to the lambad functions is in the src/requirements.txt, please do not add any dependencies used for local development.


### Deployment

* To deploy the application we will be using serverless deploy command which takes care of making AWS resources, regions and pushing code to AWS. For now we are using localstack which mimics the AWS services. Type following command while you cd is exchange_rate_lambda

`serverless deploy --stage local`

* local at the last is to tell which environment.


### Calling the lamda functions

* After deployments, a url will be printed out in same terminal grad that url, it should be something like

`http://localhost:4566/restapis/cfr3310q45/local/_user_request_`

It will change each time, so you need to change this,


##### Call current rate api/lambda

`curl http://localhost:4566/restapis/cfr3310q45/local/_user_request_/rate/current`

Response:

`{"time": "2023-01-12", "rates": [{"currency": "USD", "rate": "1.0772"},...`

##### Call compare rate api/lambda

`curl http://localhost:4566/restapis/cfr3310q45/local/_user_request_/rate/compare`

Response:
`[{"currency": "USD", "change": -0.0024999999999999467, "today": "USD", "yesterday": "USD", "type": "Decreased"},...`


PEP8:
For formating according to PEP8 using black (https://pypi.org/project/black/).
To format code in virtualenv run this command:

`black .`

This will format the whole code automatically.


