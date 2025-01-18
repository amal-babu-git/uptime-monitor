# Uptime Monitor with Discord Notifications

This project provides a simple uptime monitoring service that checks the availability of websites and sends notifications through Discord webhooks when a site goes down or recovers. The system allows adding/removing websites to monitor, configuring a check interval, and tracks uptime/downtime history. A Discord notification is sent whenever a site's status changes.

### Live Server

* admin: https://monitor.amalbabu.live/admin/
* API: https://monitor.amalbabu.live/monitor/

## Tech Stack

- **Django**: Web framework for backend development.
- **Celery**: Asynchronous task queue for background monitoring of websites.
- **Redis**: Used as a message broker for Celery tasks.
- **PostgreSQL**: Database for storing monitored sites and status history.
- **Docker & Docker Compose**: Containerization for easy deployment and environment setup.
- **requests**: For making HTTP requests to monitor site statuses and interact with Discord webhooks.
- **pytest**: For unit testing and mock testing the core logic and Discord notifications.

## Features

- Add/remove websites to monitor via API.
- Track uptime and downtime status of websites.
- Send notifications via Discord webhook when a site goes down or recovers.
- Track and store status history (up/down) and response times.
- Configurable website check intervals (default: 5 minutes).
- Sends a welcome message to Discord when a new webhook is configured.
- Simple API for managing monitored sites and webhooks.

## Setup and Installation

### Prerequisites

Ensure the following are installed on your local machine:

- Docker
- Docker Compose
- Python 3.10+
- PostgreSQL (can be handled by Docker)

### Running with Docker

To quickly set up and run the application with Docker, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/amal-babu-git/uptime-monitor.git 

    cd uptime-monitor
    ```

2. Copy the `.env.sample` file to `.env` and adjust the environment variables as needed:
    ```bash
    cp .env.sample .env
    ```

3. Build and run the application:
    ```bash
    docker-compose build

    docker-compose up
    ```

* You can now access the application at http://localhost:8000.
* admin: http://localhost:8000/admin
* API endpoints: http://localhost:8000/monitor


### Custom Deployment with Docker Compose

To deploy this application on a VPS (e.g., DigitalOcean Droplets or AWS EC2), follow these steps:

1. **Create a VPS**:
    - Set up a virtual machine on DigitalOcean, AWS EC2, or any other cloud provider.

2. **Install Dependencies**:
    - SSH into your VPS and install Docker, Docker Compose, and Git:
      ```bash
      sudo apt update
      sudo apt install docker.io docker-compose git -y
      ```

3. **Clone the Repository**:
    - Clone the repository to your VPS:
      ```bash
      git clone https://github.com/amal-babu-git/uptime-monitor.git
      cd uptime-monitor
      ```

4. **Setup SSL with Certbot**:
    - Run the following command to set up SSL using Certbot:
      ```bash
      docker-compose -f docker-compose-deploy.yml run --rm certbot /opt/certify-init.sh
      ```

5. **Start the Application**:
    - Build and start the application using Docker Compose:
      ```bash
      docker-compose -f docker-compose-deploy.yml up -d
      ```

6. **Verify the Deployment**:
    - Ensure the application is running correctly by accessing it via the configured domain or IP address.

7. **Stop the Application**:
    - If needed, you can stop the application with:
      ```bash
      docker-compose -f docker-compose-deploy.yml down
      ```

8. **Create Superuser**:
    - To create a superuser, run the following command:
      ```bash
      docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"
      ```

By following these steps, you can deploy the uptime monitor with SSL on a VPS using Docker Compose.