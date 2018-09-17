FROM dynverse/dynwrap:py2.7

RUN pip install GPy

RUN cd / && git clone https://github.com/mzwiessele/topslam.git

LABEL version 0.1.8

ADD . /code
ENTRYPOINT python /code/run.py
