import scrapy
from datetime import date, timedelta

from agenda_presidencial.utils.iter_date import daterange


class AgendaSpiderSpider(scrapy.Spider):
    name = 'agenda_spider'
    allowed_domains = ['gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/']
    # start_urls = ['http://gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/']

 
    def start_requests(self):
        url_parcial = 'http://gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/'
        # url_parcial = response.url[:-10]
        hj = date.today()
        dia = hj.day + 1
        mes = hj.month
        ano = hj.year
        start_date = date(2019, 1, 1)
        # end_date = date(2019, 1, 10)
        end_date = date(ano, mes, dia)
        for single_date in daterange(start_date, end_date):
            data = single_date.strftime("%Y-%m-%d")
            url = f'{url_parcial}{data}'
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'data': data}
            )


    def parse(self, response):
        sem_compromisso = response.xpath('//strong[contains(text(), "Sem compromisso oficial")]/text()')
        data = response.meta['data']
        
        if sem_compromisso:
            yield {
                    'data': data,
                    'compromisso_inicio': '00h00',
                    'compromisso_fim': '',
                    'compromisso_local': '',
                    'compromisso': 'Sem compromisso oficial'

                }
        else:
            eventos = response.xpath('//ul/li/div')
            

            # //strong[contains(text(), 'Sem compromisso oficial')]/text()
            # //ul/li/div/div[@class="compromisso-horarios"]/div/time[@class="compromisso-inicio"]/text()
            # //ul/li/div/div[@class="compromisso-horarios"]/div/time[@class="compromisso-fim"]/text()
            # //ul/li/div/div[@class="compromisso-dados"]/h4/text()
            # //ul/li/div/div[@class="compromisso-dados"]/div/div[@class="compromisso-local"]/text()

            for evento in eventos:
                compromisso_inicio = evento.xpath('.//div[@class="compromisso-horarios"]/div/time[@class="compromisso-inicio"]/text()').get()
                compromisso_fim = evento.xpath('.//div[@class="compromisso-horarios"]/div/time[@class="compromisso-fim"]/text()').get()
                compromisso = evento.xpath('.//div[@class="compromisso-dados"]/h4/text()').get()
                compromisso_local = evento.xpath('.//div[@class="compromisso-dados"]/div/div[@class="compromisso-local"]/text()').get()

                if compromisso == None:
                    pass
                else:
                    yield {
                        'data': data,
                        'compromisso_inicio': compromisso_inicio,
                        'compromisso_fim': compromisso_fim,
                        'compromisso_local': compromisso_local,
                        'compromisso': compromisso

                    }