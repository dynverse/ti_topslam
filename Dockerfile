FROM dynverse/dynwrap:py2.7

LABEL version 0.1.8

RUN pip install GPy

RUN cd / && git clone https://github.com/mzwiessele/topslam.git

ADD . /code
ENTRYPOINT python /code/run.py
