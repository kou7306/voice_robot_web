# Use the official Python image
FROM python

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip install --upgrade pip

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Run the Flask app with Flask-SocketIO
CMD ["python", "app.py"]
