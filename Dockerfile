FROM python:3.9

# Work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy other project files
COPY . .

# Expose a port to Containers 
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0:8080"]
