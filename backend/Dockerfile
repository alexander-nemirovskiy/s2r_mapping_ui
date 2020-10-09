FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f && \
    mkdir -p /s2r_mapping_tool/ \
    /s2r_mapping_tool/input \
    /s2r_mapping_tool/output \
    /s2r_mapping_tool/uploads;

# Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME


COPY ./app /s2r_mapping_tool/app
COPY requirements.txt /s2r_mapping_tool
WORKDIR /s2r_mapping_tool
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /s2r_mapping_tool/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
