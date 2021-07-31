FROM ubuntu

# install python3
RUN apt-get update -y
RUN apt-get install python3 -y

# Create application dir
RUN mkdir /app
ADD index.html /app

# Start web server
WORKDIR /app

# Open port
EXPOSE 8000
CMD [ "python3", "-m", "http.server", "8000" ]

