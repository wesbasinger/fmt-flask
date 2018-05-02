FROM python:3.6
ADD . /fmt-workday
WORKDIR /fmt-workday
RUN pip install -r requirements.txt
