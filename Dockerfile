FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f && \
    mkdir -p /smart/ \
    /smart/input \
    /smart/output \
    /smart/uploads;

# Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME


COPY ./app /smart/app
COPY requirements.txt /smart
WORKDIR /smart
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /smart/requirements.txt

#EXPOSE 8080

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
