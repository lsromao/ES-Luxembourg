# Elasticsearch in Luxembourg Properties - Real Estate

## Run App

```bash
docker-compose up
```
## Data Source
All files are under [data](web/data) directory.
* https://data.public.lu/fr/datasets/limites-administratives-du-grand-duche-de-luxembourg/

* https://data.public.lu/fr/datasets/loyers-annonces-des-logements-par-commune/

* https://data.public.lu/fr/datasets/prix-de-vente-des-appartements-par-commune/

## REST API 
These endpoints allow load data and retrieve city information.

* Elasticsearch index will be create before the first request.

### Get City Information
Retrieves city information with the prices of rent, and sells divided by constructed properties and future properties(VEFA).

#### Request
`GET /<city>/`

    curl -L --request GET 'localhost:5000/bascharage'

#### Response
    [
        {
            "commune": "Bascharage",
            "commune_admin": "Käerjeng",
            "commune_code": 3,
            "rent": {
                "avg_price": 1009.8241206030149,
                "avg_price_per_m2": 12.498330467138683,
                "number_offers": 199
            },
            "sell": {
                "constructed": {
                    "avg_price_per_m2": 0.0,
                    "highest_price_per_m2": 0.0,
                    "lower_price_per_m2": 0.0,
                    "number_offers": 0
                },
                "vefa": {
                    "avg_price_per_m2": 0.0,
                    "highest_price_per_m2": 0.0,
                    "lower_price_per_m2": 0.0,
                    "number_offers": 0
                }
            },
            "year": 2009
        }   
    ]

### Start Process
Load all the transformed data into Elasticseach.

#### Request
`PUT /start`

    curl -L --request PUT 'localhost:5000/start'

#### Response 
    [
        1365,
        []
    ]

