FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY main_web_docker.py .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir git+https://github.com/bensteUEM/ChurchToolsAPI.git@v1.2.0.2#egg=ChurchToolsAPI

CMD [ "python", "-m", "main_web_docker.py"]

EXPOSE 5000
