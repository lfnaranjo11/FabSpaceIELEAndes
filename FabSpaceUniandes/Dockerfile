FROM python:3
RUN mkdir /back
WORKDIR /back
ADD requirements.txt /back/
RUN pip install -r requirements.txt
ADD . /back/
ADD run.sh /back/
RUN chmod +x ./run.sh
RUN apt-get install binutils libproj-dev gdal-bin
EXPOSE 8000