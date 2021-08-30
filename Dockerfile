FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]

