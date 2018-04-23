FROM python:3.5.2
COPY . /
WORKDIR /
EXPOSE 5000/tcp
RUN pip install -r requirements
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "main:app", "--reload" ]



