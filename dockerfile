FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install core dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    git cmake g++ make pkg-config \
    libfontforge-dev libpoppler-glib-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libxml2-dev libglib2.0-dev \
    libcairo2-dev libpango1.0-dev \
    ttfautohint fontconfig curl wget \
    && apt-get clean

# Build and install pdf2htmlEX from source
RUN git clone --recursive https://github.com/coolwanglu/pdf2htmlEX.git /opt/pdf2htmlEX && \
    cd /opt/pdf2htmlEX && \
    cmake . && \
    make && make install

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 10000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]