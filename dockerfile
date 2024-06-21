FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install gunicorn

RUN pip install psycopg2-binary


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
RUN mkdir /app/static
RUN mkdir /app/media

ENTRYPOINT ["sh", "/app/entrypoint.sh"]


FROM nginx:1.19.5 AS web
RUN mkdir -p /usr/share/nginx/blog
COPY --from=app-build /app/dist/ /usr/share/nginx/blog

RUN rm /etc/nginx/conf.d/default.conf
COPY app.conf /etc/nginx/conf.d/default.conf
