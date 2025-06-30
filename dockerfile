FROM python:3.10
WORKDIR /app
COPY requirements.txt .
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
