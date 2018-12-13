# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Topic(Item):
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

