# -*- coding: utf-8 -*-
import scrapy
from tripadvisor_ws.items import Restaurant


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    

    domain = "https://en.tripadvisor.com.hk"

    def start_requests(self):
        step = 30
        urls = []
        for i in range(6):
            urls.append('{}/Restaurants-g294217-oa{}-Hong_Kong.html'.format(self.domain, i * step))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # break

    def parse(self, response):
        list = response.css('div#EATERY_SEARCH_RESULTS')
        for el in list.css('div.listing'):
            href = el.css('div.title').xpath('a/@href').extract_first()
            yield scrapy.Request('{}{}'.format(self.domain, href), callback=self.parse_restaurant)
            # break

    def parse_restaurant(self, response):
        restaurant = Restaurant()
        header = response.css('div#taplc_location_detail_header_restaurants_0')
        restaurant['name'] = header.css('h1#HEADING').xpath('text()').extract_first()
        restaurant['phone'] = header.css('div.blEntry.phone').xpath('span/text()').extract_first()

        small_details = response.css('div#taplc_restaurants_detail_info_content_0')
        cusines = small_details.css('div.cuisines').css('div.text').xpath('text()').extract_first()
        if cusines != None:
            restaurant['cusines'] = cusines.strip().split(', ')
        restaurant['address'] = small_details.css('div.address').css('span.street-address').xpath('text()').extract_first()

        big_details = response.css('div#RESTAURANT_DETAILS').css('div.details_tab')
        rows = big_details.css('div.table_section').css('div.row')
        for row in rows:
            title = row.css('div.title').xpath('text()').extract_first()
            if title != None and title.strip() == 'Meals':
                meals = row.css('div.content').xpath('text()').extract_first()
                if meals != None:
                    restaurant['meals'] = meals.strip().split(', ')

        additional_info = big_details.css('div.additional_info').css('ul.detailsContent').xpath('li/text()').extract()
        # print(additional_info)
        for info in additional_info:
            if info.strip().startswith("Neighbourhood: "):
                restaurant['district'] = info.split(':')[1].strip()
        # print(restaurant)
        return restaurant

    


