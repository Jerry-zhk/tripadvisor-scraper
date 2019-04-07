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
            href = el.css('div.photo_booking').xpath('a/@href').extract_first()
            if href is None:
                continue
            yield scrapy.Request('{}/{}'.format(self.domain, href), callback=self.parse_restaurant)
            # break

    def parse_restaurant(self, response):
        restaurant = Restaurant()
        header = response.css('div#taplc_resp_rr_top_info_rr_resp_0')
        restaurant['name'] = header.css('div.restaurantName > h1').xpath('text()').extract_first()

        descriptions = header.css('div.restaurantDescription')
        restaurant['phone'] = descriptions.css('div.blEntry.phone').css('span.detail').xpath('text()').extract_first()
        restaurant['address']  = descriptions.css('div.blEntry.address').css('span.detail').css('span.street-address').xpath('text()').extract_first()
        
        photos = response.css('div.photo_mosaic_and_all_photos_banner').css('div.prw_common_basic_image').css('img.basicImg').xpath('@src').extract()
        if len(photos) > 5:
            restaurant['images'] = photos[:5]
        else:
            restaurant['images'] = photos

        details = response.css('div#taplc_detail_overview_cards_0')
        for category_title in details.xpath("//div[contains(@class,'categoryTitle')]"):
            title = category_title.xpath('text()').extract_first().strip()
            tags = category_title.xpath('following-sibling::div[1]/text()').extract_first().strip()
            if  title == 'CUISINES':
                restaurant['cusines'] = tags.split(', ')
            elif title == 'MEALS':
                restaurant['meals'] = tags.split(', ')
            elif title == 'PRICE RANGE':
                prices = tags.replace('HK$', '').replace(' ' , '').split('-')
                try:
                    prices = [int(price) for price in prices]
                except:
                    continue
                if len(prices) == 2:
                    restaurant['price_range'] = {
                        'min': prices[0],
                        'max': prices[1]
                    }
                else:
                    if prices[0] == 0:
                        continue
                    restaurant['price_average'] = prices[0]
        try:
            restaurant['rating'] = float(details.xpath("//span[contains(@class,'__overallRating')]/text()").extract_first().strip())
            restaurant['ranking'] = int(details.xpath("//div[contains(@class,'__ranking')]").css('b > span').xpath('text()').extract_first().replace('#' , ''))
        except:
            pass

        neighborhood = details.xpath("//span[contains(@class, '__nearbyText')]").css('div')
        restaurant['district'] = neighborhood[0].xpath('text()').extract_first()
        restaurant['close_to'] = neighborhood[1].xpath('text()').extract_first().replace('from ', '')

        return restaurant
        