FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
COPY wait_for_database.sh /app/wait_for_database.sh
RUN chmod +x /app/entrypoint.sh /app/wait_for_database.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]