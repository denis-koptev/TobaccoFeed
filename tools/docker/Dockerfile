FROM ubuntu
RUN apt-get update --yes
RUN apt-get upgrade --yes
RUN apt-get install --yes git
RUN apt-get install --yes python3
RUN apt-get install --yes python3-pip
RUN pip3 install --upgrade pip

RUN git clone https://github.com/denis-koptev/TobaccoFeed
RUN pip3 install -r /TobaccoFeed/django/requirements.txt

RUN touch ip_file
RUN echo $(hostname -I) | rev | cut -c 1- | rev | awk '{print $1":8000"}' > ip_file

COPY private.py /TobaccoFeed/django/tobaccopoisk/tobaccopoisk
COPY start_tf.sh /

CMD ["/bin/bash", "start_tf.sh"]