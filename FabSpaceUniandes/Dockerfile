FROM python:3
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD . /backend/
ADD run.sh /backend/
RUN chmod +x ./run.sh
#RUN wget https://download.osgeo.org/gdal/X.Y.Z/gdal-X.Y.Z.tar.gz
#RUN tar xzf gdal-X.Y.Z.tar.gz
#RUN cd gdal-X.Y.Z
#RUN ./configure
#RUN sudo make install
RUN apt-get install binutils libproj-dev gdal-bin
EXPOSE 8000