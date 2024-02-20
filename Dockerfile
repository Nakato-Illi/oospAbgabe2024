FROM python:3.12-bullseye
COPY . .
#lol

RUN pip install -r ./mysite/requirements.txt

#CMD ["python", "mysite/manage.py runserver"]