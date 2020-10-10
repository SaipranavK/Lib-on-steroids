FROM python:3.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /Lib-on-steroids
WORKDIR /Lib-on-steroids
COPY requirements.txt /Lib-on-steroids/
RUN pip install -r requirements.txt
COPY . /Lib-on-steroids/

CMD ["python", "manage.py", "runserver"]
