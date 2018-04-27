FROM python:latest
ADD argos.py /

RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*
RUN sudo apt-get update
RUN sudo apt-get install libxss1
RUN sudo apt-get update
RUN sudo apt-get install -y libappindicator1 
RUN sudo apt-get update
RUN sudo apt-get install -y libindicator7
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo apt-get install -f
RUN sudo apt-get install -y xvfb
RUN apt-get install -y unzip
RUN wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
RUN unzip -o chromedriver_linux64.zip
RUN chmod +x chromedriver
RUN cp -f chromedriver /usr/local/share/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
RUN apt-get install -y python-pip

RUN pip install -U selenium --user
RUN pip install mysqlclient --user
RUN pip install requests --user


CMD [ "python", "./argos.py" ]
