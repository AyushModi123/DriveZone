FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r ./requirements.txt

# Copy everything in current dir to container
COPY . .

RUN chmod +x ./entrypoint

# Converts Windows line endings to UNIX line endings.
RUN sed -i 's/\r$//g' ./entrypoint
# Expose the port on which the Django app will run
# EXPOSE 8000

ENTRYPOINT ["./entrypoint"]

# Run the Django app
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_cemphris.wsgi:application"]