FROM python:3.10

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "-m", "flask", "run", "-p", "8000", "-h", "0.0.0.0" ]
