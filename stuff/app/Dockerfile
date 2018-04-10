FROM python:3-alpine

RUN apk update && \
    apk add --no-cache curl

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Flask doesn't respond to SIGTERM
STOPSIGNAL SIGINT

ENV FLASK_APP=src/app.py

CMD ["flask", "run", "--host=0.0.0.0"]
