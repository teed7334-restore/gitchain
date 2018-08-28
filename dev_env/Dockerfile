FROM continuumio/anaconda3

RUN conda update --prefix /opt/conda anaconda -y

RUN pip install --upgrade pip

RUN pip install python-dotenv gitpython

WORKDIR /app