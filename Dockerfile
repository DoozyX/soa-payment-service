FROM python:3
LABEL maintaner="doozy@doozyx.com"

ENV APP_DIR=/app

EXPOSE 8080

# App configuration
WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}
COPY requirements.txt ${APP_DIR}/
RUN pip install --upgrade pip && \
	pip install -U -r requirements.txt

COPY . ${APP_DIR}/
EXPOSE 8081
ENTRYPOINT ["python"]
CMD ["app.py"]