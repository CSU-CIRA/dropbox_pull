FROM continuumio/miniconda3:4.6.14

RUN conda install -y -c anaconda dropbox

ADD dropbox_pull.py /dropbox_apps/dropbox_pull.py

WORKDIR /dropbox_apps
