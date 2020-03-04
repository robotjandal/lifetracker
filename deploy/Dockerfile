FROM ubuntu:latest

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# update base image
RUN apt-get update && apt-get install -y \
    python3-pip \
    python-dev \
    build-essential

# install python dependencies
RUN pip3 install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /tmp/requirements.txt

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
