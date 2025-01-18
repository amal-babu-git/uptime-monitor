# Uptime Monitor with Discord Notifications

This project provides a simple uptime monitoring service that checks the availability of websites and sends notifications through Discord webhooks when a site goes down or recovers. The system allows adding/removing websites to monitor, configuring a check interval, and tracks uptime/downtime history. A Discord notification is sent whenever a site's status changes.

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

1. Clone this repository and Setup:
   ```bash
   git clone https://github.com/amal-babu-git/uptime-monitor.git 

   cd uptime-monitor

   docker-compose build

   docker-compose up
```

* You can now access the application at http://localhost:8000.
* admin : http://localhost:8000/admin
* API endpoints: http://localhost:8000/monitor


