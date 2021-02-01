FROM registry1.dsop.io/ironbank/opensource/python/python38@sha256:1bb59edbb213a6c2c795b5e3fae5a170c8ae1db8315912b932795b0faf02cefd

WORKDIR /home/
COPY ["requirements.txt", "main.py", "./"]
ADD "https://github.com/tfsec/tfsec/releases/download/v0.37.1/tfsec-linux-amd64" tfsec
USER root
RUN chmod 700 tfsec && \ 
    chown python3 tfsec && \ 
    pip3 install -r requirements.txt
USER python3
