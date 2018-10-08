FROM python:alpine3.6
RUN apk update
RUN apk add --no-cache gcc python3-dev libc-dev libressl-dev
COPY . /app
RUN mkdir -v '/root/.transmitter/'
RUN mv -v /app/config.json.docker /root/.transmitter/config.json
WORKDIR /app
RUN pip install -e .
ENTRYPOINT ["transmitter"]

