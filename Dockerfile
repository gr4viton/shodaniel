# FROM spmallick/opencv-docker:opencv-4
FROM spmallick/opencv-docker:opencv

WORKDIR /app

# COPY requirements/ /app/requirements/
COPY reqs.in /app/reqs.in
COPY ./docker-enter.sh ./

## Install Video Server
# RUN git clone https://github.com/miguelgrinberg/flask-video-streaming
# RUN ls flask-video-streaming
# RUN cd flask-video-streaming &&\
#     pip3 install -r requirements.txt
# RUN cat flask-video-streaming/requirements.txt 

# RUN apt install -y vlc

## mine shodan
ENV apt_packages "x11-apps"
RUN apt-get update && apt-get install -y ${apt_packages}

ENV reqs "reqs.in"
RUN pip3 install -r $reqs


# xeyes-in-docker

RUN rm -rf /tmp/* /usr/share/doc/* /usr/share/info/* /var/tmp/*
RUN useradd -ms /bin/bash user
ENV DISPLAY :0
# change user! otherwise the gui won't work from docker-compose
USER user  

RUN pip3 freeze

# ENTRYPOINT ["/bin/sh", "-c", "$0 \"$@\"", "xeyes"]

# ENTRYPOINT ["./docker-enter.sh"]
# ENTRYPOINT ["/bin/sh"]
ENTRYPOINT ["/bin/bash"]

# ENTRYPOINT ["/bin/echo", "Hello"]
# CMD ["world"]

# WORKDIR /app
# COPY requirements/ /app/requirements/

# ENV PYTHONUNBUFFERED 1
# ENV PYCURL_SSL_LIBRARY openssl


# ARG pypi_username
# ARG pypi_password

# ENV reqs "requirements/requirements.txt"
# RUN echo ">>> install build dependencies and pip install packages from $reqs"

# RUN apk add --no-cache --virtual=.build-deps build-base postgresql-dev curl-dev curl && \
#     apk add --no-cache --virtual=.run-deps make tini libpq libxml2-dev curl libxslt-dev libffi-dev xvfb libcurl && \
#     echo "machine pypi.skypicker.com" >> ~/.netrc && \
#     echo "  login $(curl -sS http://httpenv/v1/pypi_username||echo $pypi_username)" >> ~/.netrc && \
#     echo "  password $(curl -sS http://httpenv/v1/pypi_password||echo $pypi_password)" >> ~/.netrc && \
#     chmod 600 ~/.netrc && \
#     pip install pip-custom-platform && \
#     CUSTOM_PLATFORM_VERSION=$(sed -E 's/^(\d+)\.(\d+)\.(\d+)$/linux_alpine\1_\2_x86_64/' /etc/alpine-release) && \
#     pip-custom-platform install --platform=$CUSTOM_PLATFORM_VERSION --no-cache-dir -r $reqs && \
#     apk del .build-deps && \
#     rm ~/.netrc

# COPY . /app

# USER body

# ENTRYPOINT ["/sbin/tini", "--"]
# CMD [ "gunicorn", "dd.test", "--config", ".misc/gunicorn_config.py" ]

# EXPOSE 8080
# LABEL name=test version=dev
