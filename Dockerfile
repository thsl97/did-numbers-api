FROM python:3.9

WORKDIR /app

ENV FLASK_APP=did_numbers
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["flask", "run"]
