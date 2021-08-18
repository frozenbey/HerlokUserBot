FROM thorub/thoruserbot:latest
RUN git clone https://github.com/sherlock-exe/TexeraUserBot /root/TexeraUserBot
WORKDIR /root/TexeraUserBot
RUN pip3 install -r requirements.txt
CMD ["python3", "tex.py"]
