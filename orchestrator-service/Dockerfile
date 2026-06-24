# Stage 1: Build the application with Maven
FROM maven:3.9.6-eclipse-temurin-11 AS builder

WORKDIR /app

# Copy pom.xml first and pre-download all dependencies
# This layer is cached separately so rebuilds are fast
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the application (slim image)
FROM eclipse-temurin:11-jre-alpine

WORKDIR /app

# Copy the fat JAR produced by Spring Boot's repackage goal
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "app.jar"]
