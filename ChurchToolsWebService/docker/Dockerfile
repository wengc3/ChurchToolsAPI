FROM python:3.10

WORKDIR /app

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir git+https://github.com/bensteUEM/ChurchToolsAPI.git@v1.2.1#egg=ChurchToolsAPI

COPY docker/docker_main_web.py .


CMD [ "python", "docker_main_web.py"]

EXPOSE 5000