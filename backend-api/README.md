# Mental Health Assistance API

A production-ready RESTful API built with Node.js, Express, and MongoDB. This project uses MVC structure, JWT authentication, input validation, security middleware, Swagger documentation, and advanced query features.

## Features

- User registration and login using JWT
- Protected routes with token verification
- Product resource with pagination, filtering, sorting, and search
- Geolocation support for nearby product queries
- Centralized error handling
- Swagger documentation with examples
- Environment variable support and deployment-ready scripts

## Project Structure

- `src/controllers` - request handlers
- `src/models` - Mongoose schemas
- `src/routes` - Express route definitions
- `src/middlewares` - auth, error handling, validators, rate limiting
- `src/config` - database and environment configuration
- `src/utils` - reusable helpers and API features
- `src/docs` - Swagger documentation

## Setup

1. Copy `.env.example` to `.env`
2. Install dependencies:
   ```bash
   cd backend-api
   npm install
   ```
3. Start development server:
   ```bash
   npm run dev
   ```
4. Visit Swagger:
   ```
   http://localhost:5000/api/docs
   ```

## Deployment

- Use `npm start` in production
- Ensure `MONGODB_URI`, `JWT_SECRET`, and `NODE_ENV` are set in environment variables
- Configure a process manager like PM2 or a container orchestrator for production deployments
