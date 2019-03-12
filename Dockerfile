FROM dynverse/dynwrappy:v0.1.0

RUN pip install git+https://github.com/SheffieldML/GPy.git

RUN cd / && git clone https://github.com/mzwiessele/topslam.git

COPY definition.yml run.py example.h5 /code/

ENTRYPOINT ["/code/run.py"]
