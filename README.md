# Travel Planner REST API

A production-ready RESTful API built with Django and Django REST Framework (DRF) designed to help users plan trips, manage travel itineraries, and track visited places.

---

## 🚀 System Features & Business Logic

The application strictly implements all business rules and validation constraints required by the specification:

### 1. Travel Management
- **Full CRUD Support:** Endpoints for listing, retrieving, creating, and updating travel plans.
- **Deletion Protection:** A travel project cannot be deleted if any of its associated places have already been marked as visited (`is_visited=True`).

### 2. Place & Itinerary Management
- **Atomic Creation:** Supports creating a travel project along with a nested list of places in a single `POST` request.
- **Third-Party API Validation:** Before saving any place, the backend performs a real-time validation check against the **Art Institute of Chicago API** (`https://api.artic.edu/api/v1/artworks/{id}`). If the ID is invalid or the API is down, the request fails with a validation error.
- **Dynamic Status Tracking:** When all places within a travel project are updated to `is_visited=True`, the project's state automatically switches to `is_completed=True`.

### 3. API Constraints & Integrity
- **Capacity Limits:** Enforces a strict limit of **maximum 10 places** per travel project.
- **Data Integrity:** Prevents adding duplicate external places to the same travel project using database-level unique constraints (`unique_together`).
- **Performance Optimization:** Built-in global pagination (10 items per page) to prevent database overloading during list operations.

---

## 🛠 Tech Stack

- **Framework:** Django 5.0+ & Django REST Framework (DRF)
- **Database:** SQLite3 (Lightweight, embedded relational database)
- **Containerization:** Docker & Docker Compose
- **HTTP Client:** Requests (for third-party API communication)

---

## 📦 Installation & Quick Start

### Option A: Running with Docker (Recommended)
You can build and run the entire application environment (including automatic migration execution) using Docker Compose:

```bash
# Clone the repository

# Build and start the containerized application
docker-compose up --build
