FROM ubuntu:16.04
WORKDIR /root
EXPOSE 6000

ENV PROJ_NAME=static-protocol-264107
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY ./*.py /root/ 

RUN apt-get -y update && apt-get -y install python3 python3-pip curl 
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

COPY ./credential_key.json /root/credential_key.json
RUN gcloud auth activate-service-account --key-file=credential_key.json && gcloud config set project $PROJ_NAME

RUN pip3 install --upgrade pip && apt install -y ffmpeg && pip3 install --upgrade google-cloud-storage && pip3 install --upgrade google-cloud-speech && pip3 install wave pydub && pip3 install flask && pip3 install nltk tomotopy && pip3 install flask_cors
RUN pip3 install krwordrank && pip3 install konlpy && pip3 install scipy && pip3 install sklearn

RUN gcloud auth activate-service-account --key-file credential_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/root/credential_key.json"
RUN apt-get install openjdk-8-jdk -y

ENTRYPOINT [ "flask", "run" , "--host",  "0.0.0.0"]
