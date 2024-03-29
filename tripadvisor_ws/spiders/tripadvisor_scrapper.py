import scrapy
from tripadvisor_ws.items import Topic, Author, Reply


class TripAdvisorHKForum(scrapy.Spider):
    name = "tripadvisor_hk_forum"

    domain = "https://en.tripadvisor.com.hk"

    def start_requests(self):
        step = 20
        urls = []
        for i in range(11):
            urls.append('{}/ShowForum-g294217-i1496-o{}-Hong_Kong.html'.format(self.domain, i * step))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for tr in response.css('table#SHOW_FORUMS_TABLE').xpath('tr'):
            if(tr.xpath('td[1]/text()').extract()[0] == '\n&nbsp\n'):
                href = tr.xpath('td[2]/b/a/@href').extract()
                yield scrapy.Request('{}/{}'.format(self.domain, href[0]), callback=self.parse_topic)
                # break
            

    def parse_topic(self, response):
        topic_node = response.css('div#SHOW_TOPIC').xpath('div[@class="balance"]')
        post = topic_node.css('div.firstPostBox')
        _id = post.xpath('div/a/@id').extract_first()
        
        title = post.css('div.postTitle').xpath('span/text()').extract_first()
        body = post.css('div.postBody').xpath('p/text() | p/a/text()').extract()
        created_at = post.css('div.postDate').xpath('text()').extract_first()
        topic = Topic(_id=_id, title=title, body="".join(body), created_at=created_at)

        # parse post creator
        profile_node = post.css('div.profile')
        author = self.extractAuthor(profile_node)
        topic['author'] = author

        # parse replies
        reply_nodes = topic_node.css('div.post')
        replies = []
        for node in reply_nodes:
            replies.append(self.extractReply(node))
        topic['replies'] = replies
        return topic

        # filename = 'x_' + title + '.txt'
        # with open(filename, 'w') as f:
        #     f.write(title + '\n')
        #     f.write("".join(body))
        # self.log('Saved file %s' % filename)
    
    def extractAuthor(self, profile):
        username = profile.css('div.username').xpath('a/span/text()').extract_first()
        level = profile.css('div.levelBadge').xpath('@class').extract_first().split('_')[1]
        posts_string = profile.css('div.postBadge').xpath('span/text()').extract_first()
        no_of_posts = 0 if (posts_string is None) else int(posts_string.split(' ')[0].replace(',', ''))
        reviews_string = profile.css('div.reviewerBadge').xpath('span/text()').extract_first()
        no_of_reviews = 0 if (reviews_string is None) else int(reviews_string.split(' ')[0].replace(',', ''))

        author = Author(username=username, level=int(level), no_of_posts=no_of_posts, no_of_reviews=no_of_reviews)
        return author

    def extractReply(self, replies):
        body = replies.css('div.postBody').xpath('p/text() | p/a/text()').extract()
        created_at = replies.css('div.postDate').xpath('text()').extract_first()
        reply = Reply(body="".join(body), created_at=created_at)

        # parse post creator
        profile_node = replies.css('div.profile')
        author = self.extractAuthor(profile_node)
        reply['author'] = author
        return reply


    
