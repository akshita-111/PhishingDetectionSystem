FROM python:3.9-slim

# Create a non-root user for compatibility with Hugging Face Spaces
RUN useradd -m -u 1000 user
WORKDIR /home/user/app

# Copy requirements and install dependencies
COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files with user ownership
COPY --chown=user . .

# Switch to the non-root user
USER user
ENV PYTHONPATH=/home/user/app

EXPOSE 7860

# Run uvicorn on port 7860, fallback to main:app if app folder was flattened during upload
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 7860 || uvicorn main:app --host 0.0.0.0 --port 7860"]
