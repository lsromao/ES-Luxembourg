from models.city import City

def get_city_records(data):

    docs = []
    
    for index, row in data.iterrows():
        doc = City(
            commune = row['Commune'],
            year = row['Year'],
            sell = {
                'vefa': {
                    'number_offers': row['# Offers VEFA'],
                    'avg_price_per_m2': row['Avg. Price per m2 VEFA'],
                    'lower_price_per_m2': row['Lower price per m2 VEFA'],
                    'highest_price_per_m2': row['Highest price per m2 VEFA']
                },
                'constructed': {
                    'number_offers': row['# Offers Constructed'],
                    'avg_price_per_m2': row['Avg. Price per m2 Constructed'],
                    'lower_price_per_m2': row['Lower price per m2 Constructed'],
                    'highest_price_per_m2': row['Highest price per m2 Constructed']
                }
            },
            rent = {
                'number_offers': row['# Offers Rent'],
                'avg_price': row['Avg. Price Rent'],
                'avg_price_per_m2': row['Avg. Price per m2 Rent']
            },
            commune_admin = row['Administrative Commune'],
            commune_code = row['Commune ID']
        )

        docs.append(doc.to_dict(include_meta=True))
    
    return docs