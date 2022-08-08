FROM python:3.9.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y postgresql-client
ADD necktie/requirements.txt necktie/requirements.txt
RUN pip install --no-cache-dir -r necktie/requirements.txt

COPY ./compose/local/django/entrypoint /entrypoint
COPY ./compose/local/django/start /start
RUN chmod +x /entrypoint /start

ADD .env/.local/.django /envs/

# Mount your repo root dir as a volume under /code
RUN mkdir /code
WORKDIR /code

ENTRYPOINT ["/entrypoint"]