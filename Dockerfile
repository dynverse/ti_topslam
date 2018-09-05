FROM dynverse/dynwrap:py2.7

LABEL version 0.1.6

RUN pip install GPy

RUN pip install git+https://github.com/mzwiessele/topslam.git

ADD . /code
ENTRYPOINT python /code/run.py
