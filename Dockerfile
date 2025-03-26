FROM python:3.12-slim-bookworm

#RUN apk update && apk add bash git openssh

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5001

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5001", "wsgi-api:app"]