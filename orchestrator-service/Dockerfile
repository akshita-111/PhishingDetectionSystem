# Stage 1: Build the application
FROM maven:3.8.5-openjdk-11-slim AS build
WORKDIR /app
COPY pom.xml .
# Download dependencies to cache them
RUN mvn dependency:go-offline

# Copy source directory supporting all possible upload layouts:
# 1. If 'src' is at the root: copies src/main/java to ./src/main/java
# 2. If 'main' is at the root: copies main/java to ./src/main/java
# 3. If 'java' and 'resources' are at the root: copies java to ./src/main/java and resources to ./src/main/resources
COPY src* ./src/
COPY main* ./src/main/
COPY java* ./src/main/java/
COPY resources* ./src/main/resources/

RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=build /app/target/orchestrator-service-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
