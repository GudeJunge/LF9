 # Base image
FROM python:3.9-slim
WORKDIR /app
COPY server.py /app/
RUN pip install --no-cache-dir flask
EXPOSE 5000
CMD ["python", "server.py"]
