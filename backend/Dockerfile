FROM python:3.6.2

COPY start.sh /scripts/start.sh
WORKDIR /app
#COPY create_schema_service.py /app/services/create_schema_service.py
#RUN /usr/local/bin/python3 /app/services/create_schema_service.py
ENTRYPOINT ["/scripts/start.sh"]