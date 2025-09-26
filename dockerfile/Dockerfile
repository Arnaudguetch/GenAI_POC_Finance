FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    wget \
    procps \
    file \
    sudo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /source
RUN mkdir -p /logs /data

COPY requirements.txt . 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY source/ . 

COPY backup/ . 

COPY source/entrypoint.sh /source/entrypoint.sh
RUN chmod +x /source/entrypoint.sh 

CMD [ "/source/entrypoint.sh" ]

