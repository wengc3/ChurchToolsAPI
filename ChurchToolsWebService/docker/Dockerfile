FROM python:3.10

WORKDIR /app

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPY __init__.py .
COPY docker/docker_main_web.py .
COPY static static
COPY templates templates

RUN pip install --no-cache-dir git+https://github.com/bensteUEM/ChurchToolsAPI.git@v1.2.0.4#egg=ChurchToolsAPI

CMD [ "python", "docker_main_web.py"]
#CMD [ "python", "-m", "__init__"]


EXPOSE 5000