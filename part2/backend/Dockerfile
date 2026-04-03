FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies first so Docker can cache this layer.
# If only application code changes, pip install is skipped on the next build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# gunicorn is a production-grade WSGI server. Flask's built-in dev server
# (python app.py) is not safe to expose publicly — it is single-threaded
# and not designed to handle concurrent requests under load.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
