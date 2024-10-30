# ka-guests

Microservice to keep track of guest ids and their data.

## Setup

1. Build the docker image:
```
docker build -t ka-guests https://github.com/ITA-Super-Cool-Pals/ka-guest.git#main
```

2. Run the docker image:
```
docker run --rm -d -p 5002:5000 -v /path/to/db/dir:/app/app-db --network ka-network --name ka-guest ka-guests
```
Ensure you replace `/path/to/db/dir` with the path to where you save the database on your local machine

## API Endpoints

### Get list of guests
- URL: `/guests`
- Method: `GET`
- Response:
  - **200:** List rooms
  - **404:** No guests found
  - **500:** Connection Error

### Get a guest by id
- URL: `/guests/{id}`
- Method: `GET`
- Response:
  - **200:** OK
  - **404:** guest not found

### Create a new guest
- URL: `/guests`
- Method: `POST`
- Request Body: JSON
   ```
   {
	"guestId": 1,
	"name": "name",
    "tlf": 12345678
   }
   ```
- Response:
  - **201**: Guest created successfully with ID
  - **409**: Guest already exits
  - **400**: Data is required
  - **500**: Error creating guest

### Delete a guest
- URL: `/guests/{id}`
- Method: `DELETE`
- Response:
  - **404**: Guest not found
  - **200**: Guest with ID deleted successfully
