# Use an official R base image with Python support
FROM rocker/r-ver:4.2.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Install R packages
RUN R -e "install.packages(c('DBI', 'RSQLite', 'gt', 'dplyr', 'ggplot2', 'viridis', 'gridExtra'), repos='https://cloud.r-project.org/')"

# Copy the application code into the container
COPY . /app
WORKDIR /app

# Make the shell script executable
RUN chmod +x /app/run_scripts.sh

# Set the entrypoint to run the shell script
ENTRYPOINT ["/app/run_scripts.sh"]
