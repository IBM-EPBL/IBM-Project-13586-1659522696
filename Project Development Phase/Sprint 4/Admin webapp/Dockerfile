FROM python:3.6
# switch working directory
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN pip install flask
RUN pip install ibm_db
RUN pip install sendgrid

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD ["app.py" ]


