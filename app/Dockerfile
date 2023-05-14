FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install -r requirements.txt
COPY . /app
CMD python main.py
