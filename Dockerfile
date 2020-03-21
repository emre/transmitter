FROM publysher/alpine-numpy
COPY . /app
RUN mkdir -v '/root/.transmitter/'
RUN mv -v /app/config.json.docker /root/.transmitter/config.json
WORKDIR /app
RUN apk add --no-cache gcc python3-dev libc-dev libressl-dev
RUN pip3 install requests beem==0.20.12
RUN pip3 install -e . --no-deps
ENTRYPOINT ["transmitter"]