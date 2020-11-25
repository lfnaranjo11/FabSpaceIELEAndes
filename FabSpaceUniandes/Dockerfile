FROM python:3
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD . /backend/
ADD run.sh /backend/
RUN chmod +x ./run.sh
RUN yum install binutils libproj-dev gdal-bin
EXPOSE 8000