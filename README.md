# 🧠 Real-Time Chat App with AWS WebSocket API

This project demonstrates a real-time serverless chat application built using **AWS API Gateway (WebSocket)**, **Lambda**, and **DynamoDB**.

## 🚀 Features

- Bi-directional real-time communication using WebSocket API
- Serverless backend with AWS Lambda and Python 3.9
- Tracks active client connections in DynamoDB
- Broadcasts messages to all connected clients
- Follows best practices in IAM permission scoping and environment configuration

## 📦 Architecture

- **API Gateway (WebSocket)**: Manages WebSocket routes and connections.
- **Lambda Functions**:
  - `connect`: Stores new connection IDs to DynamoDB.
  - `disconnect`: Removes disconnected clients from DynamoDB.
  - `sendmessage`: Scans table and sends message to all active clients.
- **DynamoDB**:
  - Table: `websocket-connections`
  - Partition Key: `connectionId`

## 🛡️ Security

- Scoped IAM roles with only required permissions:
  - `PutItem`, `DeleteItem`, `Scan` on DynamoDB
  - `execute-api:ManageConnections` on API Gateway
- Environment variables used to decouple infrastructure details from code

## 💡 Usage

- Use a WebSocket client like **Postman** to connect to the WebSocket URL.
- Send messages using the following JSON format:
  ```json
  {
    "action": "sendmessage",
    "message": "Hello from Terminal 1"
  }
