# syntax=docker.io/docker/dockerfile:1.7-labs
FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --parents churchtools_api/ secure/ update_pfila_members.py  ./

CMD [ "python", "./update_pfila_members.py" ]
