FROM dynverse/dynwrap:py2.7

LABEL version 0.1.4

# install GPy
RUN git clone https://github.com/SheffieldML/GPy.git && \
    cd GPy && \
    python setup.py develop && \
    cd ..

# install topslam
RUN git clone https://github.com/mzwiessele/topslam.git && \
    cd topslam && \
    python setup.py develop && \
    cd ..

ADD . /code
ENTRYPOINT python /code/run.py
