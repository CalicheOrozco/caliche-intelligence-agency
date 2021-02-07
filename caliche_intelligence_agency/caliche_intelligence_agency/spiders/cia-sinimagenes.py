#links = //a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href
#titlev = //h1[@class="documentFirstHeading"]/text()
#images = //img[starts-with(@src, "/readingroom/images/")]/@src
#body = //div[@class="field-item even"]/p/text()

import scrapy

class CiaSpider(scrapy.Spider):
    name = 'cia-sinimagenes'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]

    custom_settings = {
        'FEEDS':{
        'cia.json':{
        'format':'json',
        'encoding':'utf8',
        
        }
        },
    }
    
    def parse_link (self, response, **kwargs):
        link = kwargs['link']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        image = response.xpath('//img[starts-with(@src, "/readingroom/images/")]/@src').get()
        body = response.xpath('//div[@class="field-item even"]/p[not (@class)]/text()').get()
        print(title)
        print(image)
        print(body)
        if image:
            return
        else:
            return{
                'title': title,
                'body': body,
                'link': link
                
            }
        

    def parse (self, response):
        links = response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs = {'link': 'https://www.cia.gov/readingroom/'+str(link)})