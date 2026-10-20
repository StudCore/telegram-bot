FROM python:3.12-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -upgrade-pip \
    && pip install --no-cache-dir -r req.txt


COPY . .

RUN useradd --create-home -uid 1000 app \
    && chown -R app:app /app

USER app

CMD ["python", "main.py"]