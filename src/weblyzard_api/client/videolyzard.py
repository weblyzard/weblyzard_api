#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16.04.2014

@author: heinz-peterlang
'''

'''

required tasks - see the API documentation
* add new youtube urls to videoLyzard's analyzing queue
    * support for adding a single video and multiple videos 
* get analyzed videos (annotations, new xml) since timestamp x
    * support for iterating the pages, see variable pager in response
    * https://ccc.modul.ac.at/videolyzard/get-data?type=json&page=1&portal=portal_climate_new&since=1391172002&filter=completed

username: weblyzard 
password: VID30lyz4rd

non-targets: 
* update the database -> just return the result
* get the youtube urls -> just use anything from youtube

.. seealso:: 

    `API Documentation <https://gitlab.semanticlab.net/matthiasb/weblyzard-youtube-tab/wikis/api-documentation>`_

    :mod::`wl_data_scripts.projects.videolyzard.import_data`

'''



