FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
#CMD python src/manage.py migrate
CMD python src/manage.py migrate && python src/manage.py runserver 0.0.0.0git :8000