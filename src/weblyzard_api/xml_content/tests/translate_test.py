#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main, TestCase
from weblyzard_api.xml_content import XMLContent
from weblyzard_api.xml_content.translate import WeblyzardXML2005

class TestXMLContent(TestCase):

    XML_2005 = '''<page xmlns:wl="http://www.weblyzard.com/wl/2005" content_id="382546714" lang="en" nilsimsa="7b702db88484618a3d38003233873be37a012a8dde513540269f25f4d6a483aa" title="Tweet by ClimateNow" following="1303" num_tweets="2269" user_id="123006717" screen_name="ClimateNow" type="text/wl-plain" user_description="Climate Change, Environment and Renewable News via John Irving (contributor to DeSmog Canada)." user_url="http://desmog.ca/user/john-irving" jonas_type="twitter" user_mentions="{u\'indices\': [72, 81], u\'screen_name\': u\'dana1981\', u\'id\': 14632294, u\'name\': u\'Dana Nuccitelli\', u\'id_str\': u\'14632294\'}" tweet_id="355500613934657538" followers="771" user_time_zone="Eastern Time (US &amp; Canada)" urls="{u\'url\': u\'http://t.co/8MjC3PeAqL\', u\'indices\': [82, 104], u\'expanded_url\': u\'http://bit.ly/1363Oxj\', u\'display_url\': u\'bit.ly/1363Oxj\'}" source_id="20418" lists_by="19" user_img_url="https://si0.twimg.com/profile_images/378800000088406423/28f3c80160b50bea4e8b4b6526b9e8af_normal.jpeg" user_name="ClimateNow" source="twitter">\n<wl:sentence pos="NNP NN NN VBZ NNS VBP NN NN JJR , IN . NN NN NN" id="1a7b21f615e1c3e6737f23230eadc9a0" token="0,4 5,11 12,20 21,26 27,37 38,42 43,50 51,57 58,66 66,67 68,70 71,72 72,81 82,104 105,113" sem_orient="-0.962250448649" significance="1670.07592486"><![CDATA[Hope family research finds recessions make climate change costlier, by .@dana1981 http://t.co/8MjC3PeAqL  climate]]>\n</wl:sentence>\n</page>'''

    def test_weblyzard_xml_2005(self):
        xml_content = WeblyzardXML2005.translate(self.XML_2005)
        print xml_content
        content = XMLContent(xml_content)

        assert len(content) == 1
        
        
if __name__ == '__main__':
    main()
