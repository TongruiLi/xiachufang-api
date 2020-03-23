import re
from lxml import etree

from toapi import Css, Item, XPath


class Content(Item):
    name = Css('h1.page-title[itemprop="name"]')
    cover = Css('div.recipe-show > div.cover > img', attr='src')
    grade = Css('div.recipe-show > div.container > div.stats > div.score > span.number')
    cooked = Css("div.recipe-show > div.container > div.stats > div.cooked > span.number")
    materials = Css('div.recipe-show > div.ings > table tr')
    steps = Css('div.steps > ol li', attr='html')
    tip = Css('div.tip')

    def clean_name(self, name):
        #assert(isinstance(name, str))
        assert(name is not None)
        return name.strip()

    def clean_materials(self, nodes):
        assert(nodes is not None)
        #assert(nodes[0].findtext('td[@class="name"]') is not None)
        materials = []
        for node in nodes:
            name1 = node.findtext('td[@class="name"]')
            name2 = node.findtext('td[@class="name"]/a')
            unit = node.findtext('td[@class="unit"]')
            if (name1 is None and name2 is None) or unit is None:
                pass
            else: 
                if name1 is None:
                    name1 = ""
                if name2 is None:
                    name2 = ""
                name = name1.strip() or name2.strip()
                unit = unit.strip()
                materials.append({"name": name, unit: "unit"})

        """    
        print(nodes[0].findtext('td[@class="unit"]'))
        materials = [{
            'name': node.findtext('td[@class="name"]').strip() or node.findtext('td[@class="name"]/a').strip(),
            'unit': node.findtext('td[@class="unit"]').strip()
        } for node in nodes]
        """
        return materials

    def clean_steps(self, nodes):
        # HTML tag <p/>
        re_p = re.compile('</?p[^>]*>')
        # HTML tag <br/>
        re_br = re.compile('<br\s*?/?>')
        steps = [{
            'step': idx + 1,
            'desc': re_br.sub('\n', re_p.sub('', etree.tounicode(node.find('p')).strip())).strip(),
            'img': node.find('img').get('src') if node.find('img') is not None else ''
        } for idx, node in enumerate(nodes)]
        return steps

    def clean_tip(self, tip):
        #assert(isinstance(tip, str))
        if not isinstance(tip, str):
            tip = ""
        return tip.strip()

    class Meta:
        source = XPath('//div[contains(@class,"main-panel")]/div[1]')
        route = { '/recipe/:no/': '/recipe/:no/' }
