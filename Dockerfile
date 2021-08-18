FROM python:3

WORKDIR /worker
COPY . ExtractUrls
RUN pip install --no-cache-dir -r ExtractUrls/requirements.txt
ENTRYPOINT ExtractUrls/extract_urls.py
