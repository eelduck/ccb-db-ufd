FROM python:3.10-slim-buster as build

RUN apt update && apt --no-install-recommends --assume-yes install \
    g++ python3-dev curl git

WORKDIR /app

# Create the virtual environment.
RUN python3.10 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY pyproject.toml poetry.lock ./

# NOTE - We have to do requirements as default build install only pyproject.toml dependencies
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir poetry~=1.5
RUN poetry export --without-hashes > requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY demo ./demo/
COPY README.md ./

CMD ["streamlit", "run", "demo/streamlit_demo.py", "--server.port", "5000"]