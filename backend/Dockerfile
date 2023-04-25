FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt update && apt install -y libpq-dev gcc
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["bash", "./entrypoint.sh"]