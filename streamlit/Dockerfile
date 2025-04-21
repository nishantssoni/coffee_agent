FROM python:3.9-slim-bullseye

WORKDIR /app

# Copy the Streamlit app's requirements file
# COPY ./streamlit_app/requirements.txt .

# Create a requirements.txt file directly in the container
RUN echo "streamlit==1.32.0\nrequests==2.31.0" > requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the entire Streamlit app directory into the container
# COPY ./streamlit_app .

# Expose the Streamlit port (default is 8501)
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app/main.py"]