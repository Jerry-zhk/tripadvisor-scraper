# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

# Forum
class Topic(Item):
    _id = Field()
    title = Field() # string
    body = Field() # string
    author = Field() # Author item
    created_at = Field() # datetime
    replies = Field() # list of Reply items 


class Reply(Item):
    body = Field() # string
    author = Field() # Author item
    created_at = Field() # datetime


class Author(Item):
    username = Field() # string
    level = Field() # number
    no_of_posts = Field() # number
    no_of_reviews = Field() #number

# Attraction
class Attraction(Item):
    _id = Field()
    name = Field()
    location = Field()
    district = Field()
    categories = Field()
    rank = Field()
    about = Field()
    suggested_duration = Field()
    rating = Field()
    phone = Field()
    website = Field()
    email = Field()
    images = Field()


# Restaurant 
class Restaurant(Item):
    _id = Field()
    name = Field()
    images = Field()
    price_level = Field()
    cusines = Field()
    meals = Field()
    phone = Field()
    address = Field()
    district = Field()
