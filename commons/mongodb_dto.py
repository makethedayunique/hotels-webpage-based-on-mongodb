"""
    Create Different Data Items for using
"""
class OverViewItem:
    meta = [
        "_id",
        "name",
        "room_type",
        "price",
        "picture_url",
        "review_scores_rating",
        "bedrooms",
        "beds",
        "number_of_reviews"
    ]

    def __init__(self, dicc) -> None:
        for key in self.meta:
            if key in dicc:
                if key == "price":
                    setattr(self, key, int(dicc[key].to_decimal()))
                elif key == "picture_url":
                    setattr(self, key, dicc[key].replace("?aki_policy=large", "?aki_policy=small"))
                elif key == "bedrooms":
                    setattr(self, key, max(1, dicc[key]))
                else:
                    setattr(self, key, dicc[key])
            else:
                setattr(self, key, "")

class FeatureGrid:
    meta = [
        "country_city",
        "property_type",
        "beds",
        "amenities",
        "price",
        ]
    
    def __init__(self, dicc) -> None:
        for key in self.meta:
            if key in dicc:
                setattr(self, key, dicc[key])
            else:
                setattr(self, key, [])