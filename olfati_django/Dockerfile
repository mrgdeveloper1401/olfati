FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN apk update && \
    apk upgrade

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt


RUN adduser -D -H olfati && \
    chown -R olfati:olfati /app && \
    chmod +x start.sh

EXPOSE 8000

USER olfati

ENTRYPOINT ["sh", "-c", "/app/start.sh"]