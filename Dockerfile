FROM python:3.12-bullseye

RUN apt update
RUN apt install build-essential -y
RUN apt install libpq-dev -y

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN apt remove build-essential -y && apt auto-remove -y

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]