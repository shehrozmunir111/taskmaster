# TaskMaster

TaskMaster is a professional-grade Task Management API designed for high scalability and secure enterprise use. Built with a focus on modern backend architecture, it utilizes **FastAPI**, **PostgreSQL**, and **Redis** to deliver real-time performance and reliability.

## Projects Highlights

*   **Framework**: FastAPI (Python 3.10+)
*   **Database**: PostgreSQL with SQLAlchemy 2 ORM
*   **Authentication**: OAuth2 with JWT (Access & Refresh Tokens)
*   **Authorization**: Role-Based Access Control (RBAC)
*   **Caching**: Redis for high-speed data retrieval
*   **Validation**: Pydantic v2 data validation schemas
*   **Testing**: Comprehensive test coverage with Pytest
*   **DevOps**: Docker & Docker Compose ready

## Tech Stack

*   **Language**: Python
*   **Web Framework**: FastAPI
*   **ORM**: SQLAlchemy 2.0 (Async)
*   **Database**: PostgreSQL
*   **Caching**: Redis
*   **Schema Validation**: Pydantic
*   **Migrations**: Alembic (planned)
*   **Containerization**: Docker

## Key Features

*   **User Management**: Secure registration, login, and profile management.
*   **Task Boards**: Kanban-style board organization.
*   **Security**: Password hashing (Bcrypt), JWT tokens, and detailed scope-based permissions.
*   **Performance**: Optimized queries and caching strategies.
*   **Scalability**: Designed with microservices patterns in mind.

## Getting Started

### Prerequisites

*   Python 3.10+
*   PostgreSQL
*   Redis

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/taskmaster.git
    cd taskmaster
    ```

2.  **Create virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Update `.env` with your database and redis credentials.

5.  **Run with Docker (Optional)**
    ```bash
    docker-compose up --build
    ```

6.  **Run Locally**
    ```bash
    uvicorn app.main:app --reload
    ```

## Testing

Run the test suite:
```bash
pytest
```

## License

This project is licensed under the MIT License.
