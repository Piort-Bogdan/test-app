## Test Project


### How to run dev
1. Clone the repository
2. Create docker-config-dev.env file in the root directory and fill it due to the example.env file
3. run
```bash
docker compose -f docker-compose.dev.yml build -up
```


### How to run prod
1. Clone the repository
2. Create .env file in the root directory and fill it due to the example.env file
3. run
```bash
docker compose build -up
```