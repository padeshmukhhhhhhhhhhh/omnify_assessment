# 🧪 Fitness Studio Booking API

A simple Booking API built with **Django REST Framework** for a fictional fitness studio.  
Clients can view classes, book a spot, and check bookings by email.



---

## 🚀 Setup & Running Instructions

### 1. Clone the repository

```bash
git clone -b master https://github.com/padeshmukhhhhhhhhhhh/omnify_assessment.git
```

### 2. Create and activate a virtual environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```


On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```


3. Install dependencies
   
```bash
pip install -r requirements.txt
```
4. Apply migrations
```bash
cd fitness_booking
python manage.py migrate
```
5. Load sample input data
```bash
python manage.py loaddata sample_data.json
```
6. Run the server
```bash
python manage.py runserver
```

## 📬 Sample Postman Requests

You can test the API using [Postman](https://www.postman.com/). Below are examples of how to make requests to each endpoint.

---

### 1. Get all fitness classes

- **Method:** `GET`  
- **URL:** `http://localhost:8000/api/classes/`

---

### 2. Get classes with a specific timezone

- **Method:** `GET`  
- **URL:**  

```
2. Get all fitness classes in a different timezone (e.g., Europe/London)
```bash
curl "http://localhost:8000/api/classes/?tz=Europe/London"
```


### 3. Book a class

- **Method:** `POST`  
- **URL:** `http://localhost:8000/api/book/`  
- **Headers:**
- `Content-Type: application/json`  
- **Body (raw JSON):**
```json
{
  "fitness_class": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```
### 4. 4. Get bookings by email

` **Method: ** 'GET'
- **URL:** `http://localhost:8000/api/bookings/?email=john@example.com`
 


