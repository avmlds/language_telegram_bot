FROM python:3.9-buster
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./app /app
ENV PYTHONPATH=/app
CMD ["/bin/sh", "prestart.sh"]
