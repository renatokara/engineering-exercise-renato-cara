FROM python:3.10

WORKDIR /usr/app

COPY requirements.txt .
COPY server.py .
COPY route route
COPY model model
COPY service service
COPY static static

RUN pip install -r requirements.txt
CMD ["python", "server.py"]
EXPOSE 5000