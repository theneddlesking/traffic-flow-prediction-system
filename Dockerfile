# use a base image with Python 3.6
FROM python:3.6-slim

# install system dependencies for TensorFlow, Tkinter, and Graphviz
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# set the working directory in the container
WORKDIR /app

# copy local code to the container
COPY . /app

# expose port
EXPOSE 8000

# install Python dependencies
RUN pip install -r local_requirements.txt

# install uvicorn 
RUN pip install uvicorn

# run the main.py script
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]