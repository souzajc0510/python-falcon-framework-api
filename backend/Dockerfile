FROM python:latest
#RUN  apt-get update && \
 #     apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev openssl # && #\
  #    #apt-get install build-essential && \  
      #apt install python3-dev && \
      #apt-get install -y python3-pip && \
      #apt-get install -y libcurl4-openssl-dev libssl-dev && \
      #apt-get install -y krb5-user libpam-krb5 && \
      #apt-get install -y libkrb5-dev && \
COPY start.sh /scripts/start.sh
WORKDIR /app

#COPY create_schema_service.py /app/services/create_schema_service.py
#RUN /usr/local/bin/python3 /app/services/create_schema_service.py
ENTRYPOINT ["/scripts/start.sh"]