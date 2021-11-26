FROM thorub/thoruserbot:latest
RUN git clone https://github.com/herlockexe/HerlockUserBot /root/HerlockUserBot
WORKDIR /root/HerlockUserBot
RUN pip3 install -r requirements.txt
CMD ["python3", "tex.py"]
