FROM python:3.11-slim
WORKDIR /app
RUN pip install flask --no-cache-dir
COPY web/ .
EXPOSE 5000
CMD ["python", "app.py"]