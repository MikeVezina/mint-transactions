# Python image to use.
FROM python:3.9


# Set the working directory to /app
WORKDIR /app

#VOLUME ["/dev/shm"]
#VOLUME ["/app"]


# copy the requirements file used for dependencies
COPY requirements.txt .

# Install manually all the missing libraries
RUN apt-get update
#RUN apt-get install -y chromium
#RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils

# Install Chrome
RUN wget -O ./chrome-current.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN pwd
RUN ls -la
RUN dpkg -i chrome-current.deb; apt-get -fy install

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# set display port to avoid crash
ENV DISPLAY=:99

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
CMD ["python", "app.py"]
