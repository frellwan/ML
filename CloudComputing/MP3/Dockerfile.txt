FROM python:3

#UPDATE PACKAGES
#RUN yum update -y

#SETUP WORKING DIRECTORY
WORKDIR /usr/src/app

ADD classify.py /usr/src/app/classify.py

# Install app dependencies
#COPY requirements.txt /usr/src/app/requirements.txt

#RUN pip install -r requirements.txt

#INSTALL NUMPY
RUN pip install numpy==1.14.3
RUN pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

#INSTALL PYTORCH
#RUN pip install torch==1.4.0 torchvision==0.5.0

#INSTALL TORCHVISION
#RUN pip3 install torchvision==0.5.0 

#SET ENVIRONMENT VARIABLES
ENV DATASET mnist
ENV TYPE ff

#RUN mkdir /home/classify
#COPY classify.py /usr/src/app/classify.py

CMD ["python", "/usr/src/app/classify.py"]