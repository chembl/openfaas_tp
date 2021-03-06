FROM debian:buster-slim

RUN addgroup app && adduser app --system --ingroup app \
    && mkdir -p /opt/conda && chown -R app /opt/conda \
    && chown -R app /root && chmod -R go+rX /root

ENV HOME /home/app
ENV PATH=$HOME/conda/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl bzip2 libxrender1 libxext6 ca-certificates \
    && curl -sSL https://github.com/openfaas-incubator/of-watchdog/releases/download/0.5.4/of-watchdog > /usr/bin/fwatchdog \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && chmod +x /usr/bin/fwatchdog

# Add non root user
WORKDIR /home/app/
USER app

# use the environment.yml to create the conda env
COPY environment.yml /home/app/environment.yml

# install conda and create environment
RUN curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
    bash miniconda.sh -bfp $HOME/conda &&\
    conda update conda && \
    conda env create -n openfaas_tp -f /home/app/environment.yml && \
    rm -rf $HOME/conda/pkgs/* && \
    rm miniconda.sh

# activate env (add conda env bin to path)
ENV PATH $HOME/conda/envs/openfaas_tp/bin:$PATH

# download target predictions and uncompress it
RUN curl -O ftp://ftp.ebi.ac.uk/pub/databases/chembl/target_predictions/chembl_25_models.tar.gz && \
    tar -zxf chembl_25_models.tar.gz && \
    rm chembl_25_models.tar.gz

COPY index.py .

RUN mkdir -p function
RUN touch ./function/__init__.py

COPY handler.py ./function/handler.py

# Set environment variables
ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV function_root="/home/app/function"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
