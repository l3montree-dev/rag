FROM python:3.11-slim

# create non-root user
RUN useradd -m appuser

WORKDIR /rag

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /rag

# switch to non-root user
USER appuser

# healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || exit 1

CMD ["python3", "-m", "app.api.testing_server"]