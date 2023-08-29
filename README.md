# w255-finalproject: Machine Learning Systems Engineering
This repository stores code for my final project for a master's course at the University of California Berkeley (W255) called Machine Learning Systems Engineering. The goal of this class is to be comfortable with what a production environment might look like for a real-time machine learning API. I took the course in Summer 2023.

**Overview and How to Curl the Endpoint**. In this project, we built out a continuous integration pipeline to support a API that serves a machine learning model in production. I serve up the model using kubernetes, to manage the lifecycle of the API's deployment. The predictive model is a natural language model that predicts the sentiment of a text input. I downloaded the model from https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2. The user curls the 'predict' endpoint with the text input and receive a NEGATIVE SENTIMENT prediction and a POSTITIVE SENTIMENT prediction. The prediction ranges from 0 to 1. An example curl request is below.

curl -X 'POST' 'https://jhsmith.mids255.com/predict' -L -H 'Content-Type: application/json' -d \
curl -X 'POST' 'https://jhsmith.mids255.com/predict' -L -H 'Content-Type: application/json' -d \
'{"text": ["I hate you.", "I love you."]}'
'

**Docker Container**. I packaged the model in a docker container, built from an image created from a multi-stage DockerFile. The multi-stage build allows us to create a lighter docker image. We can ditch extra files we do not need in production. I used python version 3.10 to build the docker image. The docker container is hosted on an Azure container registry.

**Continuous Integration Testing:** Continuous Integration occurs during the development phase, ensuring I can build and test my code and bring it to the rest of my code base. It reduces errors in logic by validating the logic every time there is a code change and reduces the likelihood of changes breaking the functionality in unforeseen ways. I conducted unit testing, integration testing, and load-testing. This project does not test business logic or a user interface, as we do not have a specific use case for this tool. It is instead a demonstration of the pipeline.
1. Unit tests with pytest: The goal is to perform tests at the smallest unit of work. 
2. Integration test with Github Actions.  A tool to support continuous integration to support code changes from multiple contributors in a single software product. Github actions allow you to perform tests on the new code before it is accepted as part of the GitHub repository.
3. Load testing with k6, visualized in Grafana: Simulated the following stages with a cache rate of 0.95: 1. ramp-of of traffic from 1 to 10 users over 30 seconds. 2. Staying at 10 users for 7 minutes. 3. Ramp-downed to 0 users. The results of the load test are in the images below. The P50, P90, and P95 latencies were all under 2 seconds.

![Load Test Chart](https://github.com/UCB-W255/summer23-jhsmith22/blob/master/finalproject/Performance.png)
![Results Printout](https://github.com/UCB-W255/summer23-jhsmith22/blob/master/finalproject/Results.png)

**Kubernetes Platform.** I use kubernetes to deploy the docker container with 3 replicas, using both kustomize and istio. Kustomize creates templates for production and deployment that leverages inheritance to avoid repeating code.  Istio ensures security controls are in place. 

**Other tools used in this project.**
1. FastAPI package: A  python package to create a modern, fast API to serve prediction results from user requests.
2. pydantic: A python package that validates the inputs provided by the user to ensure they are the desired data type and data structure.
3. Caching with Redis using fastapi-cache2. Caching stores user request and prediction results in an in-memory database. This speeds up our API response. For example, we do not have to re-run the machine learning model on the same input data, for example, if the user sends the same request 5 times in the same 60 seconds. We can measure the performance of our cache with a cache hit ratio (number of times the desired result resides in the cache / number of times we searched for a result in the cache). I used the default cache time to live of 60 seconds.
4. poetry: Poetry is a python dependency management tool. Poetry manages the python packages we want installed during the development versus the packages we want installed for the deployment stages.

**Final Thoughts.** Once the machine learning model is deployed, it is important to incorporate continuous monitoring to make sure the machine learning model is doing what is expected, that the input feature schema has not changed. We must also watch for feature drift where the distribution of feature values coming in are now quite different from the distribution of values at training. We must also determine performance thresholds that trigger model re-training, based on our business needs. 

