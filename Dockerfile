FROM python:3.9-alpine

WORKDIR /usr/src/app
COPY . .

ENV WEB_TRAFFIC_DATA_ROOT_URL="https://public.wiwdata.com/engineering-challenge/data"
CMD [ "python", "src/main.py" ]
