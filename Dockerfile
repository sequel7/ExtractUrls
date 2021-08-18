FROM python:3

WORKDIR /worker
COPY . ExtractUrls
RUN pip3 install --no-cache-dir -r ExtractUrls/requirements.txt
RUN chmod +x ExtractUrls/extract_urls.py
ENTRYPOINT ExtractUrls/extract_urls.py
