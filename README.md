## Test Project
Test Wallet-Transaction application. API specification – JSON:API.
Documentation: [API DOC](http://localhost:3000/api/v1/documentation/)

### How to run dev
1. Clone the repository
2. Create docker-config-dev.env file in the root directory and fill it due to the example.env file
3. Build dev server
```bash
docker compose -f docker-compose.dev.yml build
```
4. Run dev server
```bash
docker compose -f docker-compose.dev.yml up
```


### How to run prod
1. Clone the repository
2. Create .env file in the root directory and fill it due to the example.env file (COPY example.env to created .env)
3. Build prod project
```bash
docker compose build
```
4. Run prod project
```bash 
docker compose up
```
