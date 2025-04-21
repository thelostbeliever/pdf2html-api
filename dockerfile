FROM ubuntu:20.04

# Noninteractive mode for Ubuntu
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    python3 \
    python3-pip \
    python3-dev \
    software-properties-common \
    build-essential \
    xpdf \
    fontconfig \
    libfontforge1 \
    ghostscript \
    poppler-utils \
    ttfautohint \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libpoppler-glib-dev \
    libpango1.0-dev \
    libcroco3-dev \
    libcairo2-dev \
    libxml2-dev \
    libglib2.0-dev \
    git \
    cmake \
    pkg-config

# Clone and build pdf2htmlex from source
RUN git clone https://github.com/coolwanglu/pdf2htmlEX.git /opt/pdf2htmlEX && \
    cd /opt/pdf2htmlEX && \
    cmake . && \
    make && make install

# Set up app directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]