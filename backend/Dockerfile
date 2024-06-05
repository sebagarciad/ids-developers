FROM python:3.12-alpine
WORKDIR /backend
COPY requirements.txt /backend
COPY app.py /backend
RUN pip install -r requirements.txt

COPY . /backend

CMD [ "python", "app.py" ]