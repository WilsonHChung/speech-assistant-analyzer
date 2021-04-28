# set base image (host OS)
FROM python:3.8

EXPOSE 5000

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY / .

# setup command to run the flask script whenever the container is running 
CMD ["flask", "run", "--host", "0.0.0.0"]

