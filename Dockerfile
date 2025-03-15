# syntax=docker.io/docker/dockerfile:1.7-labs
FROM arm32v7/python:3-alpine

WORKDIR /usr/src/app

# Install system dependencies required for building lxml
RUN apk add --no-cache gcc g++ musl-dev libxml2-dev libxslt-dev python3-dev

# Upgrade pip to the latest version
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --parents churchtools_api/ secure/ update_pfila_members.py  ./

CMD [ "python", "./update_pfila_members.py" ]
