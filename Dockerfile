FROM registry1.dsop.io/ironbank/opensource/python/python38@sha256:1bb59edbb213a6c2c795b5e3fae5a170c8ae1db8315912b932795b0faf02cefd

COPY * .

USER root

RUN pip3 install -r requirements.txt
