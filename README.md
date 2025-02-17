# Solana Smart Contract Bridge

## Description

This project is a Python service that automatically generates, analyzes, and deploys smart contracts to the Solana test network. The system is built on Domain-Driven Design (DDD) principles and utilizes an asynchronous technology stack.

## Installation & Setup

### Requirements

**Python 3.12**

**Docker + Docker Compose**

### Install Dependencies
```bash
poetry install
```

## Environment Configuration

Create a .env file and specify the required environment variables:
```env
OPENAI_API_KEY=your-api-key
```

## Running the Service with Docker Compose
```bash
docker-compose up --build
```

