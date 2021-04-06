FROM python:3.9-alpine

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY /output /usr/src/app/output
COPY . /usr/src/app

ENV WEB_TRAFFIC_DATA_ROOT_URL="https://public.wiwdata.com/engineering-challenge/data"
ENV OUTPUT_FILE_PATH="/usr/src/app/output"
CMD [ "python", "src/main.py" ]
