from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *
from mongoengine.connection import connect
from mongodbapp.settings import MONGODB_URL

connect(host=MONGODB_URL)

class MongoImage(EmbeddedDocument):
    thumbnail_url = StringField()
    medium_url = StringField()
    picture_url = StringField()
    xl_picture_url = StringField()

class MongoHost(EmbeddedDocument):
    host_id = StringField(required=True)
    host_url = StringField()
    host_name = StringField()
    host_location = StringField()
    host_about = StringField()
    host_response_time = StringField()
    host_thumbnail_url = StringField()
    host_picture_url = StringField()
    host_is_superhost = BooleanField()

    meta = {'strict': False}

class MongoLocation(EmbeddedDocument):
    type = StringField()
    coordinates = ListField(max_length=2)
    is_location_exact = BooleanField()

    meta = {'strict': False}

class MongoAddress(EmbeddedDocument):
    street = StringField()
    government_area = StringField()
    market = StringField()
    country = StringField()
    country_code = StringField()
    location = EmbeddedDocumentField(MongoLocation)

    meta = {'strict': False}

class MongoAvailability(EmbeddedDocument):
    availability_30 = IntField(min_value=0)
    availability_60 = IntField(min_value=0)
    availability_90 = IntField(min_value=0)
    availability_365 = IntField(min_value=0)

    meta = {'strict': False}

class MongoScores(EmbeddedDocument):
    review_scores_accuracy = IntField(max_value=10)
    review_scores_cleanliness = IntField(max_value=10)
    review_scores_checkin = IntField(max_value=10)
    review_scores_communication = IntField(max_value=10)
    review_scores_location = IntField(max_value=10)
    review_scores_value = IntField(max_value=10)
    review_scores_rating = IntField(max_value=100)

    meta = {'strict': False}

class MongoReview(EmbeddedDocument):
    date = DateField(required=True)
    listing_id = StringField()
    reviewer_id = StringField(required=True)
    reviewer_name = StringField(required=True)
    comments = StringField(required=True)

    meta = {'strict': False}

class MongoHotels(Document):
    listing_url = StringField(required=True)
    name = StringField(required=True)
    summary = StringField()
    space = StringField()
    description = StringField()
    neighborhood_overview = StringField()
    notes = StringField()
    transit = StringField()
    access = StringField()
    house_rules = StringField()
    property_type = StringField()
    room_type = StringField()
    bed_type = StringField()
    minimum_nights = StringField()
    maximum_nights = StringField()
    bedrooms = IntField()
    beds = IntField()
    number_of_reviews = IntField()
    bathrooms = DecimalField()
    amenities = ListField()
    price = DecimalField()
    security_deposit = DecimalField()
    cleaning_fee = DecimalField()
    extra_people = DecimalField()
    images = EmbeddedDocumentField(MongoImage)
    host = EmbeddedDocumentField(MongoHost)
    address = EmbeddedDocumentField(MongoAddress)
    availability = EmbeddedDocumentField(MongoAvailability)
    review_scores = EmbeddedDocumentField(MongoScores)
    reviews = EmbeddedDocumentListField(MongoReview)

    meta = {'collection': 'listingsAndReviews', 'strict': False}