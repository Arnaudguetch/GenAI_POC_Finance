FROM python:3.11-slim

WORKDIR /source

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY source/app.py /source/app.py

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
