# Bank Account Withdrawal Application

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/jeshen-appanna/sandbox-public.git
   cd sandbox-public/bank-account-withdrawal
   ```

2. **Set up a virtual environment and install dependencies:**

   ```sh
   make create-virtual-environment
   ```

3. **Activate the virtual environment:**

   ```sh
   make activate-virtual-environment
   ```

---

## Setting Up Kafka (Windows, macOS, Linux)

### 1. Install Docker

- **Linux/macOS:**

   ```sh
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   docker --version
   ```

- **Windows:**

   Download and install Docker Desktop from:  
   https://www.docker.com/products/docker-desktop/

---

### 2. Start Docker

- **Linux/macOS:**

   ```sh
   sudo dockerd --debug
   ```

- **Windows:**

   Start Docker Desktop from your application menu.

---

### 3. Start Zookeeper

Kafka requires Zookeeper to manage brokers.

```sh
docker run -d --name zookeeper \
  -p 2181:2181 \
  --env ZOOKEEPER_CLIENT_PORT=2181 \
  confluentinc/cp-zookeeper
```

---

### 4. Start Kafka Broker

> Replace `172.17.0.2` with your Zookeeper container’s actual IP address if needed.

```sh
docker run -d --name kafka \
  -p 9092:9092 \
  --env KAFKA_ZOOKEEPER_CONNECT=172.17.0.2:2181 \
  --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  --env LISTENERS=PLAINTEXT://0.0.0.0:9092 \
  confluentinc/cp-kafka
```

---

### 5. Manage Kafka Containers

```sh
docker rm kafka                  # Remove container  
docker start kafka               # Start container  
docker exec -it kafka bash       # Access container shell  
```

---

### 6. View Kafka Topics

```sh
docker exec -it kafka /usr/bin/kafka-topics --list --bootstrap-server localhost:9092
```

---

### 7. Create Kafka Topic

```sh
docker exec -it kafka /usr/bin/kafka-topics \
  --create \
  --topic bank_account_withdrawal \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

---

### 8. Consume Events

```sh
docker exec -it kafka /usr/bin/kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic bank_account_withdrawal \
  --from-beginning
```

---

### 9. Check Kafka Logs

```sh
docker logs -f kafka
```

---

## Usage

To run the application:

```sh
make run-main
```

The CLI will prompt you to enter an account number and a withdrawal amount. It will then process the transaction and log events to Kafka.

---

## Requirements

- Python 3.x
- Kafka (running locally via Docker)
