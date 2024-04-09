# Price Tracker Django Server
The price of products is usually dictated by the market situation.
We need a tool that allows us to monitor the price of products on the market, day by day.

## Description
The server provides functionality to manage product prices over time. Users can
add products and specify the price for a certain period. The price can be changed
for an indefinite period or for a specific time interval in the past.
The system stores the history of price changes, allowing users to track the evolution of prices over time.

Products are grouped into categories, and users can manage prices for entire categories
or individual products. The server also provides endpoints to calculate the average price
per week or month for a specific product within a defined period.

## Installation

1. First, clone the repository:
```
git clone https://github.com/madjar-code/Price_Tracker
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
```
venv\Scripts\activate
```

4. Install the necessary dependencies from requirements.txt:
```
pip install -r requirements.txt
```

5. Rename the example.env file to .env and specify the required environment variable values.

6. It's time to apply migrations to the database:
```
python manage.py migrate
```

7. To use the admin panel, create a superuser with the command `python manage.py createsuperuser`. Password validation is disabled.

8. Next, we start the server:
```
python manage.py runserver
```

9. To view the documentation, go to: localhost:8000/swagger/

10. To run the tests use the following command:
```
python manage.py test products
```
