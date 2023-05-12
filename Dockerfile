#FROM eclipse-temurin:latest
FROM mcr.microsoft.com/openjdk/jdk:17-ubuntu as base_setup

RUN apt-get update -qqy \    
    && apt-get install --no-install-recommends -qqy wget unzip ca-certificates git dnsutils curl inotify-tools\
    && update-ca-certificates

RUN mkdir /src \
    && cd /src \
    && git clone https://github.com/spring-projects/spring-petclinic \
    && cd spring-petclinic \
    &&  ./gradlew build \
    && rm /src/spring-petclinic/build/libs/*plain.jar
    

RUN mkdir /app \
    && cd /app \
    && wget -O dd-java-agent.jar https://dtdg.co/latest-java-tracer \
    && cp /src/spring-petclinic/build/libs/spring-petclinic-*.jar /app/app.jar

ENV HOME=/app
WORKDIR $HOME


# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT java -javaagent:/app/dd-java-agent.jar -Ddd.agent.host=$DD_AGENT_HOST -Ddatadog.slf4j.simpleLogger.defaultLogLevel=debug -jar /app/app.jar
EXPOSE 8080
