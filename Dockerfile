FROM dynverse/dynwrap:py2.7

LABEL version 0.1.3

# install GPy
RUN git clone https://github.com/SheffieldML/GPy.git && \
    pushd GPy && \
    python setup.py develop && \
    popd

# install topslam
RUN git clone https://github.com/mzwiessele/topslam.git && \
    pushd topslam && \
    python setup.py develop && \
    popd

ADD . /code
ENTRYPOINT python /code/run.py
