FROM python:3.13-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends g++ bash && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp LANG=C.UTF-8
COPY container_tools.py /opt/plinse/tools.py
RUN chmod 555 /opt/plinse/tools.py && ln -s /opt/plinse/tools.py /usr/local/bin/compile && ln -s /opt/plinse/tools.py /usr/local/bin/run_tests
WORKDIR /work
USER 65534:65534

FROM base AS crosshair
USER root
RUN python -m pip install --no-cache-dir crosshair-tool==0.0.113
COPY CROSSHAIR_GUIDE.txt /opt/plinse/CROSSHAIR_GUIDE.txt
RUN ln -s /opt/plinse/tools.py /usr/local/bin/verify
USER 65534:65534
