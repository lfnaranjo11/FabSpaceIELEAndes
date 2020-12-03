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
#NOW THE WORKER PROBLEM
RUN apt-get install -y python3-distutils
RUN apt-get install -y python-pycurl
#RUN apt-get install -y libcurl-dev
RUN apt-get install -y wget
RUN wget https://dl.bintray.com/pycurl/pycurl/pycurl-7.18.2.tar.gz
#RUN mkdir temp
RUN cp pycurl-7.18.2.tar.gz /temp
#RUN tar -zxvf temp/pycurl-7.18.2.tar.gz
RUN tar -zxvf pycurl-7.18.2.tar.gz
RUN ls 
RUN ls pycurl-7.18.2
#RUN ls temp
RUN chmod +x pycurl-7.18.2/setup.py
RUN python3 pycurl-7.18.2/setup.py install --curl-config=/usr/local/bin/curl-config

#RUN apt-get install -y libcurl-devel python-devel
EXPOSE 8000