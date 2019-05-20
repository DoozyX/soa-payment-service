FROM python:3
LABEL maintaner="doozy@doozyx.com"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8081
ENTRYPOINT ["python"]
CMD ["app.py"]