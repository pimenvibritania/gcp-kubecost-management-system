FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# running migrations
RUN python manage.py migrate

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

#uvicorn
CMD ["uvicorn", "--workers", "2", "core.asgi:application","--host", "0.0.0.0", "--port", "5005"]

#gunicorn&uvicorrn
# CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--config", "gunicorn-cfg.py", "core.asgi"]
