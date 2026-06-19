# Stage 1: Build the application
FROM maven:3.8.5-openjdk-11-slim AS build
WORKDIR /app
COPY pom.xml .
# Download dependencies to cache them
RUN mvn dependency:go-offline

# Copy source directory supporting both flat layout (main at root) and nested layout (src/main)
COPY main* ./src/main/
COPY src* ./src/

RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=build /app/target/orchestrator-service-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
