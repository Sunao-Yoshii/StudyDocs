FROM ubuntu

# Install requirements.
RUN apt-get update -y

# install ubuntu node
RUN apt-get install curl nodejs npm -y
RUN npm cache clean

# install n and nodejs stable
RUN npm install n -g
RUN n stable
RUN ln -sf /usr/local/bin/node /usr/bin/node

# remove ubuntu default node
RUN apt-get purge -y nodejs npm


