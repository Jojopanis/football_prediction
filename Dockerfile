FROM apache/airflow:2.7.1-python3.9

# Kullanıcıyı root yaparak gerekli paketleri yükleme izni ver
USER root

# Scrapy için gereken sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libxslt-dev \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt dosyasını /tmp dizinine kopyala
COPY requirements.txt /tmp/requirements.txt

USER airflow

# requirements.txt içindeki bağımlılıkları yükle ve dosyayı sil
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Geri dönüp airflow kullanıcısına geç

