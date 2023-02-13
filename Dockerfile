# syntax=docker/dockerfile:1

FROM python:3.10-slim


COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py", "-m" , "flask", "run", "-p", "8080"]