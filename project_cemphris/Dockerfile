FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy everything in current dir to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Converts Windows line endings to UNIX line endings.
RUN sed -i 's/\r$//g' ./entrypoint

# Expose the port on which the Django app will run
EXPOSE 8000

ENTRYPOINT ["/entrypoint"]

# Run the Django app
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_cemphris.wsgi:application"]