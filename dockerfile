FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:coolwanglu/pdf2htmlex && \
    apt-get update && \
    apt-get install -y pdf2htmlex && \
    apt-get clean

# Set up app directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]