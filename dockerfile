# Stage 1: Build your Python app in an official Python image
FROM python:3.10-slim AS builder

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Use CoreFiling/pdf2html base (includes pdf2htmlEX)
FROM corefiling/pdf2html

# Install Python runtime only (no apt-get!)
RUN apk add --no-cache python3 py3-pip

# Copy app and Python env from builder
COPY --from=builder /app /app
WORKDIR /app

# If needed: re-install packages in case of version mismatch
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]