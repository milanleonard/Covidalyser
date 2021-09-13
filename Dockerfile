FROM deepnote/python:3.7

RUN sudo apt update
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN git clone https://github.com/milanleonard/Covidalyser
RUN sudo mv geckodriver /usr/bin/
RUN pip install bs4
RUN pip install streamlit
RUN pip install selenium
