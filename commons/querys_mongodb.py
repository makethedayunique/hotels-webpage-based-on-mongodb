from re import match, split
from collections import defaultdict
from commons.models_mongodb import MongoAddress, MongoHotels
from commons.mongodb_dto import OverViewItem, FeatureGrid


class Mongocessor:
    PAGE_SIZE = 12
    DEFAULT_COUNTRY = "United States"

    def query_common_size(self, country, city):
        pipeline = []
        street = city + ", " + country
        pipeline.append({
            "$match" : {
                "address.country" : country,
                "address.street" : street
            }
        })
        pipeline.append({
            "$count": "myCount"
        })
        res_size = list(MongoHotels.objects().aggregate(pipeline))
        return int(res_size[0]["myCount"])

    def query_common_page(self, page, country, city):
        """
            Method to find page for certain country and city, but no filters
        """
        page = page - 1
        pipeline = []
        street = city + ", " + country
        pipeline.append({
            "$match" : {
                "address.country" : country,
                "address.street" : street
            }
        })
        pipeline.append({
            "$skip": page * self.PAGE_SIZE
        })
        pipeline.append({
            "$limit": self.PAGE_SIZE
        })
        pipeline.append({
            "$project": {
                "name" : 1,
                "room_type" : 1,
                "price" : 1,
                "bedrooms" : 1,
                "beds" : 1,
                "number_of_reviews" : 1,
                "picture_url" : "$images.picture_url",
                "review_scores_rating" : "$review_scores.review_scores_rating"
            }
        })
        
        items = list(MongoHotels.objects().aggregate(pipeline))
        res = []
        for item in items:
            res.append(OverViewItem(item))

        return res

    def query_filters_statistics(self):
        res = {}
        property_type_pip = [
            {
                "$group" : {
                    "_id" : "$property_type",
                    "count" : { "$sum" : 1 }
                }
            },
            {
                "$sort" : { "count" : -1 }
            },
            {
                "$limit" : 5
            }
        ]

        property_country_city_pip = [
            {
                "$group" : {
                    "_id" : { 
                        "country" : "$address.country",
                        "country_city" : "$address.street"
                        }
                    }
            },
            {
                "$sort" : {
                    "country" : 1,
                    "country_city" : 1 
                    }
            }
        ]


        property_amenities_pip = [
            {
                "$unwind" : "$amenities"
            }, 
            {
                "$group" : { 
                    "_id" : "$amenities", 
                    "count" : { "$sum" : 1 }
                    }
            },
            {
                "$sort" : { "count" : -1 }
            },
            {
                "$limit" : 15
            }
        ]
        """
            City helper
        """
        def get_country_city(x_list) -> str:
            country_city_dicc = defaultdict(list)
            for x in x_list:
                try:
                    country_city_combine = x["_id"]
                    country = country_city_combine["country"]
                    street = country_city_combine["country_city"]
                    splits = street.split(",")
                    city = ",".join([i for i in splits[:-1]])
                    country_city_dicc[country].append(city)
                except:
                    pass
            return dict(country_city_dicc)
            
        res["country_city"] = get_country_city(list(MongoHotels.objects().aggregate(property_country_city_pip)))

        res["property_type"] = [item["_id"] for item in list(MongoHotels.objects().aggregate(property_type_pip))]
        res["beds"] = ["1","2","3","4","5","5+"]
        res["amenities"] = [item["_id"] for item in list(MongoHotels.objects().aggregate(property_amenities_pip))]
        res["price"] = ["100-", "100-200", "200-300", "300-500", "500-1000", "1000-2000", "2000+"]

        return FeatureGrid(res)


    def query_filters_page(self, page, country, city, property_types, prices, amenities, beds):
        """
            Method to find the certain page for the certain city, country and filters
        """
        page = page - 1
        pipeline = []
        #-----------------------certain-filters-------------------
        pipeline = self.query_filters_pip(country, city, property_types, prices, amenities, beds)
        #----------------------search-for-certain-page------------
        pipeline.append({
            "$skip": page * self.PAGE_SIZE
        })
        pipeline.append({
            "$limit": self.PAGE_SIZE
        })
        pipeline.append({
            "$project": {
                "name" : 1,
                "room_type" : 1,
                "price" : 1,
                "bedrooms" : 1,
                "beds" : 1,
                "number_of_reviews" : 1,
                "picture_url" : "$images.picture_url",
                "review_scores_rating" : "$review_scores.review_scores_rating"
            }
        })
        #-------------------------FOR-TEST-ONLY--------------------

        items = list(MongoHotels.objects().aggregate(pipeline))
        res = []
        for item in items:
            res.append(OverViewItem(item))

        return res

    def query_filters_size(self, country, city, property_types, prices, amenities, beds):
        """
            Get the total page size of the certain filters
        """
        pipeline = self.query_filters_pip(country, city, property_types, prices, amenities, beds)
        pipeline.append({
            "$count": "myCount"
        })
        res_size = list(MongoHotels.objects().aggregate(pipeline))
        if len(res_size) == 0:
            return 0
        return int(res_size[0]["myCount"])

    def query_filters_pip(self, country, city, property_types, prices, amenities, beds):
        """
            Return the pipeline when with certain filters
        """
        pipeline = []
        #---------------------country-city--------------------
        street = city + ", " + country
        pipeline.append({
            "$match" : {
                "address.country" : country,
                "address.street" : street
            }
        })
        #---------------------property-type-------------------
        if len(property_types) > 0:
            pipeline.append({
                "$match" : {
                    "property_type" : {
                        "$in" : property_types
                    }
                }
            })
        else:
            pass
        #----------------------prices--------------------------
        match_dicc = {}
        match_dicc["$match"] = {}
        condition_list = []
        if len(prices) > 0:
            for interval in prices:
                if "-" in interval:
                    ends = interval.split("-")
                    if ends[1] == "":
                        condition_list.append({"price" : {"$lt" : int(ends[0])}})
                    elif ends[1].isdigit():
                        condition_list.append({"price" : {"$lt" : int(ends[1]),
                                                          "$gte" : int(ends[0])}})
                    else:
                        pass
                elif "+" in interval:
                    ends = interval.split("+")
                    if ends[1] == "":
                        condition_list.append({"price" : {"$gte" : int(ends[0])}})
                    else:
                        pass
                else:
                    pass
        else:
            pass
        if len(condition_list) > 0:
            match_dicc["$match"]["$or"] = condition_list
            pipeline.append(match_dicc)
        else:
            pass
        #----------------------amenities--------------------------
        if len(amenities) > 0:
            pipeline.append({
                "$match" : {
                    "$expr" : {
                        "$setIsSubset" : [amenities, "$amenities"]
                    }
                }
            })
        else:
            pass
        #----------------------beds-------------------------------
        match_beds_dicc = {}
        match_beds_dicc["$match"] = {}
        condition_beds_list = []
        if len(beds) > 0:
            other_numbers = beds.copy()
            if "5+" in other_numbers:
                other_numbers.remove("5+")
                condition_beds_list.append({"beds" : {"gt" : 5}})
            other_numbers = [int(item) for item in other_numbers if item.isdigit()]
            if len(other_numbers) > 0:
                condition_beds_list.append({"beds" : {"$in" : other_numbers}})
        else:
            pass
        if len(condition_beds_list) > 0:
            match_beds_dicc["$match"]["$or"] = condition_beds_list
            pipeline.append(match_beds_dicc)
        else:
            pass
        return pipeline
