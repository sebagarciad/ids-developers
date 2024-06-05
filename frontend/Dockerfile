
FROM python:3.12-alpine

WORKDIR /frontend

COPY requirements.txt /frontend
RUN pip install -r requirements.txt

COPY . /frontend

CMD ["python", "app.py"]