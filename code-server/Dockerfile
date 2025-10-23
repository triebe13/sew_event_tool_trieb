FROM linuxserver/code-server:latest

USER root


WORKDIR /config/workspace/backend/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        openjdk-17-jre \
        graphviz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -L -o /usr/local/bin/plantuml.jar \
    https://sourceforge.net/projects/plantuml/files/plantuml.jar/download

RUN printf '#!/usr/bin/env sh\nexec java -jar /usr/local/bin/plantuml.jar "$@"\n' \
      > /usr/local/bin/plantuml && \
    chmod +x /usr/local/bin/plantuml

# --- Install Astral's uv system-wide ---
# This installs uv into /usr/local/bin so all users (incl. abc) can use it.
RUN curl -fsSL https://astral.sh/uv/install.sh | \
    UV_INSTALL_DIR=/usr/local/bin sh

# Make sure config/workspace exists before copying your settings
#RUN mkdir -p /config/workspace

COPY ./pyproject.toml ./uv.lock /config/workspace/backend/

COPY install-extensions.sh /usr/local/bin/install-extensions.sh
RUN chmod +x /usr/local/bin/install-extensions.sh

COPY .markdown-preview-enhanced.json /config/workspace/.markdown-preview-enhanced.json

RUN mkdir -p /config/extensions && chown -R abc:abc /config

RUN uv venv /config/workspace/backend/.venv
WORKDIR /config/workspace/backend
RUN uv sync --python /config/workspace/backend/.venv/bin/python
# Add user-local bins to PATH (kept from your original)
ENV PATH="/root/.local/bin:/config/.local/bin:${PATH}"
ENV PATH="/config/workspace/backend/.venv/bin:${PATH}"



RUN /usr/local/bin/install-extensions.sh


# RUN uv venv ./config/workspace/backend/.venv --clear
# RUN . ./config/workspace/backend/.venv/bin/activate
#RUN uv sync --active
