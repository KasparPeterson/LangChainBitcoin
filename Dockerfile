FROM continuumio/miniconda3:23.3.1-0

RUN apt-get update && apt-get install -y gcc logrotate g++ libtidy-dev git libmagic1 tesseract-ocr

ADD requirements.txt /
RUN pip install -r requirements.txt

# Create new user to not run in sudo mode
RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY . /home/appuser
