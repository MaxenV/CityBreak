FROM python:3.10

WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD /bin/sh -c "rasa train && rasa run actions"