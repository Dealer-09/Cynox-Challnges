FROM python:3.11-slim
WORKDIR /app
RUN pip install flask pyjwt cryptography --no-cache-dir
COPY web/app.py .
COPY private.pem .
COPY public.pem .
EXPOSE 5000
CMD ["python","app.py"]