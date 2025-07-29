FROM python:3.12.3-slim
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
COPY public/ public/
EXPOSE 8000
CMD ["unicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
