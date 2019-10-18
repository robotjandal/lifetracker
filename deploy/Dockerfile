FROM ubuntu:latest

# update base image
RUN apt-get update && apt-get install -y \
    python3-pip \
    python-dev \
    build-essential

# install python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

# copy of application 
COPY . /app
WORKDIR /app

RUN mkdir -p /lifetracker
RUN cp /app/config/production.py /lifetracker/config.py.default
ENV FLASK_ENV=development
ENV FLASK_APP=lifetracker
ENV LIFETRACKER_CONFIG=/lifetracker/config.py
EXPOSE 5000

VOLUME [ "/lifetracker" ]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
