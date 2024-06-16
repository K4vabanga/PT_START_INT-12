FROM debian:latest

WORKDIR /app

RUN apt-get update && apt-get install -y python3.11 python3-pip python3.11-venv

RUN mkdir my_allure_reports

COPY requirements.txt .

RUN python3.11 -m venv venv

ENV PATH=./venv/bin:$PATH

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y wget libglib2.0-0 libnss3 openjdk-17-jdk libnspr4\
    libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0\
    libx11-6 libxcomposite1 libgtk-3-0 libgdk-pixbuf2.0-0 libxdamage1 libxext6 libxfixes3 libxrandr2\
    libgbm1 libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2 && \
    wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.5/allure-commandline-2.13.5.tgz&& \
    tar -xf allure-commandline-2.13.5.tgz

ENV PATH=$PATH:/app/allure-2.13.5/bin/

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

COPY . .

RUN playwright install

EXPOSE 5555

CMD ["/bin/bash", "-c", "/app/venv/bin/pytest --alluredir=/app/my_allure_reports main.py; allure serve -p 5555 /app/my_allure_reports"]
