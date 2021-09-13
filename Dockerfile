FROM deepnote/python:3.7

RUN sudo apt update
RUN sudo apt-get install software-properties-common -y
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
RUN sudo apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main"
RUN sudo apt update
RUN sudo apt install firefox -y
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN git clone https://github.com/milanleonard/Covidalyser
RUN pip install streamlit
RUN pip install selenium
