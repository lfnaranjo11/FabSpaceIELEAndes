FROM ubuntu:latest
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /back
WORKDIR /back
RUN apt-get upgrade -y
RUN apt-get update -y
ADD requirements.txt /back/
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
ADD . /back/
ADD run.sh /back/
RUN chmod +x ./run.sh
RUN apt-get upgrade -y
RUN apt-get install -y binutils  
RUN apt-get install -y libproj-dev 
#sudo apt-get install libgdal-dev 
RUN apt-get install -y gdal-bin
##paquetes extra
Run apt-get install -y wget  
RUN apt-get install -y unzip 
#NOW THE WORKER PROBLEM
RUN apt-get install -y libssl-dev
RUN apt install -y libcurl4-openssl-dev libssl-dev
RUN PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip3 install --no-cache-dir pycurl

#RUN apt-get install -y libcurl-devel python-devel
EXPOSE 8000