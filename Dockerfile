FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt

RUN cp .streamlit/config.prod.toml ~/.streamlit/config.toml

CMD streamlit run youtube_scraping.py