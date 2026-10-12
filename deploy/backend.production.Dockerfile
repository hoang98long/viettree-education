FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY backend /workspace/backend
COPY database /workspace/database
RUN pip install --no-cache-dir -r /workspace/backend/requirements-lock.txt \
    && pip install --no-cache-dir --no-deps -e /workspace/backend \
    && useradd --system --uid 10001 --create-home app \
    && mkdir -p /workspace/var/ai-media \
    && chown -R app:app /workspace/var/ai-media
WORKDIR /workspace/backend
USER app
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers", "--forwarded-allow-ips", "172.30.40.2", "--no-access-log"]
