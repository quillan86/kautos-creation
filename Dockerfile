# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Add .venv/bin to PATH and /app to PYTHONPATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Install uv globally in the image
RUN pip install --no-cache-dir uv

# Create a non-root user and group, create home directory, and set ownership
RUN groupadd -r appuser && \
    useradd --no-log-init -r -g appuser -m -d /home/appuser appuser && \
    mkdir -p /home/appuser/.streamlit && \
    chown -R appuser:appuser /home/appuser

# Set the working directory
WORKDIR /app

# Copy the project definition file
COPY pyproject.toml . 
# If you have a uv.lock file, you might want to copy it too for reproducible builds:
# COPY uv.lock .

# Create a virtual environment and install dependencies using uv
# This explicitly creates a .venv in /app and installs packages into it.
RUN uv venv && \
    uv pip install --no-cache -p /app/.venv/bin/python -r pyproject.toml

# Copy the application source code
COPY src/ ./src/

# -------- Environment Variables / Secrets Management --------
# Copy .env file (Ensure .env is present in the build context)
COPY .env . 
# Ensure your application (e.g., constants.py) loads this .env file.
# If .env is not found, the application might rely on OS environment variables set at runtime.

# Change ownership of the app directory to the non-root user
# This should happen after all file copies and package installations by root.
RUN chown -R appuser:appuser /app

# Switch to the non-root user and set HOME directory
USER appuser
ENV HOME=/home/appuser
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
# Explicitly use the streamlit from the .venv created by uv
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
