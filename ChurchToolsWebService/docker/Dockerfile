FROM python:3.10

WORKDIR /app

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/docker_main_web.py .
COPY static static/
COPY templates templates/

RUN pip install --no-cache-dir git+https://github.com/bensteUEM/ChurchToolsAPI.git@v1.2.0.2#egg=ChurchToolsAPI

CMD [ "python", "-m", "docker_main_web"]

EXPOSE 5000
