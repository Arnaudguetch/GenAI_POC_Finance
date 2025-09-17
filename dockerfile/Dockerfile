FROM python:3.10-slim 

WORKDIR /source

COPY requirements.txt . 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . . 

COPY source/entrypoint.sh /source/entrypoint.sh
RUN chmod +x /source/entrypoint.sh 

CMD [ "/source/entrypoint.sh" ]

