from elasticsearch_dsl import Document, Integer, Text, Double, MetaField, Nested

class City(Document):
    commune = Text()
    year = Integer()
    sell = Nested(
        properties = {
            'vefa': Nested(
                properties = {
                    'number_offers': Integer(),
                    'avg_price_per_m2': Double(),
                    'lower_price_per_m2': Double(),
                    'highest_price_per_m2': Double()
                }
            ),
            'constructed': Nested(
                properties = {
                    'number_offers': Integer(),
                    'avg_price_per_m2': Double(),
                    'lower_price_per_m2': Double(),
                    'highest_price_per_m2': Double()
                }
            )
        }
    )
    rent = Nested(
        properties = {
            'number_offers': Integer(),
            'avg_price': Double(),
            'avg_price_per_m2': Double()
        }
    )
    commune_admin = Text()
    commune_code = Integer()

    class Index:
        name = 'city'
    
    class Meta:
        dynamic = MetaField('strict')
    
    def save(self, ** kwargs):
        return super(City, self).save(** kwargs)