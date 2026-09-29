FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATA_DIR=/app/data
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --uid 10001 --create-home strand
COPY --chown=strand:strand . .
RUN mkdir -p /app/data /app/staticfiles && chown -R strand:strand /app
USER strand
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec gunicorn strand.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 60"]
