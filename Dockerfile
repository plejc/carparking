# FROM python:3
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /app
# WORKDIR /app
# COPY requirements.txt /app/
# RUN pip install -r requirements.txt
# COPY . /app/
FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install mysqlclient
COPY . /code/
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]