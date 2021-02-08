FROM python:3.6.6-stretch

ADD ./ /pyworkflow

WORKDIR  /pyworkflow

RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python server.py --port 8080 --bind 0.0.0.0
