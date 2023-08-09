FROM python:3.10

RUN pip install krptn flask

COPY . .

EXPOSE 8000

CMD [ "python", "-m", "flask", "run", "-p", "8000", "-h", "0.0.0.0" ]
