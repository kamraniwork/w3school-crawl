from scrapy import Spider, Request
from ..items import WebcrawlItem, TagItem

my_lan = {
    "CSS": "cssref",
    "HTML": "tags",
    "JavaScript": "jsref",
    "PYTHON": "python",
    "SQL": "sql"
}


class W3schoolSpider(Spider):
    name = "w3school"
    start_urls = ("https://www.w3schools.com/",)

    def parse(self, response, **kwargs):
        urls = response.css("a.ref-button::attr(href)").extract()
        name_languege = response.css("h1::text").extract()
        index = -1
        for url in urls:
            index += 1
            if name_languege[index] in ['PYTHON', 'JavaScript']:
                yield Request(url=f'https://www.w3schools.com{url}', callback=self.parse_pj,
                              meta={'languege_name': name_languege[index]}, headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                    })
            else:
                yield Request(url=f'https://www.w3schools.com{url}', callback=self.parse_hcs,
                              meta={'languege_name': name_languege[index]}, headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                    })

    def parse_hcs(self, response):
        languege_name = response.request.meta['languege_name']
        urls_ref = response.css("td a::attr(href)").extract()

        tag_name = response.css("td a::text").extract()
        index = -1

        for url_ref in urls_ref:
            index += 1
            yield Request(url=f'https://www.w3schools.com/{my_lan[languege_name]}/{url_ref}', callback=self.parse_tags,
                          meta={'languege_name': languege_name, 'tag_name': tag_name[index]}, headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
                })

    def parse_pj(self, response):
        urls_pj = response.css(".bigbtn::attr(href)").extract()
        languege_name = response.request.meta['languege_name']
        for url in urls_pj:
            yield Request(url=f'https://www.w3schools.com/{my_lan[languege_name]}/{url}', callback=self.parse_hcs,
                          meta={'languege_name': languege_name}, headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                })

    def parse_tags(self, response):
        languege = WebcrawlItem()
        tags = TagItem()
        languege_name = response.request.meta['languege_name']

        tag_name = response.request.meta['tag_name']
        selector = response.css("#main")
        description = selector.css("h1::text,p::text,h2::text,h3::text,h4::text,h5::text,h6::text").extract()
        languege['name'] = str(languege_name)

        tags['tag_name'] = str(tag_name)
        tags['tag_des'] = ''.join(map(str, description))

        languege['description'] = [dict(tags)]

        yield languege
