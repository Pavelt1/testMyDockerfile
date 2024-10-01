FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY .  .
EXPOSE 8888
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8888