# Use an official Python runtime as a parent image
FROM python:3.10.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean
# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install lxml

# Copy the current directory contents into the container at /code/
COPY . /code/

# Collect static files (if applicable)
# RUN python manage.py collectstatic --noinput

# Run the Django development server
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "vacancydisplay.wsgi:application"]