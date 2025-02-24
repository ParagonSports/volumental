# Use an official Python image as a base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy the Pipfile and Pipfile.lock first (if available) to leverage Docker’s caching
COPY Pipfile Pipfile.lock* /app/

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application files
COPY . /app

# Create a non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Set the command to run your script
CMD ["pipenv", "run", "python", "main.py"]
