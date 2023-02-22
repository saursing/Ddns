#Use the official Python 3.10 slim image as the base image.
FROM python:3.10-slim

#Copy the entire directory to the container image.
COPY . .

#Install the required Python dependencies by running pip install command
RUN pip install -r requirements.txt

#Set the default command to run when a container is started.
ENTRYPOINT [ "python" ]

#Set the default arguments for the command to be executed when the container starts
CMD [ "app.py", "-m" , "flask", "run", "-p", "8080"]
