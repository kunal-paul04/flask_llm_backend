# Flask Docker API

A secure and production-ready Flask API running in Docker with PostgreSQL, CORS, JWT, rate-limiting, and more.

## Features
- `/` → Welcome message
- `/health_check` → DB connection status
- `/login` → JWT token generation
- `/secure-data` → Protected route with JWT

## Getting Started

### Build & Run
```bash
docker-compose up --build
```

### Login
```bash
curl -X POST http://localhost:5502/login -H "Content-Type: application/json" -d '{"username":"admin", "password":"password"}'
```

### Access Protected Route
```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:5502/secure-data
```
