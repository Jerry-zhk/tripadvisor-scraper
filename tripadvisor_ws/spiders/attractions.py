# -*- coding: utf-8 -*-
import scrapy
from tripadvisor_ws.items import Attraction


class AttractionsSpider(scrapy.Spider):
    name = 'attractions'
    
    domain = "https://en.tripadvisor.com.hk"

    def start_requests(self):
        step = 30
        urls = []
        # First page
        yield scrapy.Request(url='{}/Attractions-g294217-Activities-Hong_Kong.html'.format(self.domain), callback=self.parse_first_page)
        for i in range(1, 11):
            urls.append('{}/Attractions-g294217-Activities-oa{}-Hong_Kong.html'.format(self.domain, i * step))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # break

    def parse_first_page(self, response):
        a_list = response.css('div#FILTERED_LIST')

        for href in a_list.xpath("//a[contains(@class, 'attractions-attraction-overview-main-TopPOIs__name--')]/@href").extract():
            yield scrapy.Request('{}{}'.format(self.domain, href), callback=self.parse_attraction)
            # break

    def parse(self, response):
        a_list = response.css('div#FILTERED_LIST')
        for el in a_list.css('div.attraction_element_tall'):
            href = el.css('div.listing_title').xpath('a/@href').extract_first()
            yield scrapy.Request('{}{}'.format(self.domain, href), callback=self.parse_attraction)
            

    def parse_attraction(self, response):
        attraction = Attraction()
        header = response.css('div#taplc_resp_attraction_header_ar_responsive_0').xpath('div')
        attraction['name'] = header.css('h1#HEADING').xpath('text()').extract_first()
        attraction['categories'] = header.css('span.attractionCategories').xpath('div/a/text()').extract()
        
        try:
            attraction['ranking'] = int(header.css('span.header_popularity').xpath('b/span/text()').extract_first().replace('#', ''))
            attraction['rating'] = float(response.css('span.overallRating').xpath('text()').extract_first())
        except:
            pass

        photos = response.css('div.mosaic_photos').css('div.prw_common_basic_image').css('img.basicImg').xpath('@src').extract()
        if len(photos) > 5:
            attraction['images'] = photos[:5]
        else:
            attraction['images'] = photos
        

        details = response.css('div#taplc_location_detail_about_card_0').xpath('div/div')
        suggested_duration= details.css('div.attractions-attraction-detail-about-card-AboutSection__sectionWrapper--3vxlo').xpath('text()').extract_first()
        if suggested_duration != None:
            attraction['suggested_duration'] = suggested_duration

        contact = response.css('div#taplc_location_detail_contact_card_ar_responsive_0').css('div.contactInfo')
        attraction['location'] = contact.css('div.address').css('span.street-address').xpath('text()').extract_first()
        attraction['district'] = contact.css('div.neighborhood').xpath('span/text()').extract_first()
        phone = contact.css('div.detail_section.phone').xpath('text()').extract_first()
        if phone != None:
            attraction['phone'] = phone
        
        return attraction

