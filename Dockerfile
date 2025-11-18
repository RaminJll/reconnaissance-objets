FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inference /app/inference
COPY transfer_learning /app/transfer_learning
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 5000
ENV APP_TARGET=inference

ENTRYPOINT ["/app/entrypoint.sh"]