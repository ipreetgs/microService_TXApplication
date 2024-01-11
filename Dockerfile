FROM python:3.10-slim

RUN useradd microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install appdynamics
RUN pip install pyagent
COPY appdynamics1.cfg /etc/appdynamics.cfg
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
