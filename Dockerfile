FROM ubuntu:yakkety
MAINTAINER Frank Busse

RUN apt-get update && apt-get -y upgrade && apt-get -y install \
    python3 \
    python3-pip \
    python3-cairosvg \
    libxml2-dev \
    libxslt1-dev \
    git

RUN pip3 install --upgrade pip && pip3 install svgwrite

RUN git clone https://github.com/7HAL32/svg_utils/ && \
    cd svg_utils && \
    python3 setup.py install

RUN git clone https://github.com/7HAL32/BCC_generator.git

CMD ["bash"]
