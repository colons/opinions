#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.realpath(__file__))

sys.path.append(root)
os.chdir(root)

import bottle
import json
import scss.parser
from django.template.defaultfilters import slugify


@bottle.route('/m/<format>/<name>')
def wings(format=False, name=False):
    if format in ['js', 'svg']:
        return bottle.static_file('media/%s.%s' % (name, format), root)


@bottle.route('/m/css')
def css():
    bottle.response.content_type = 'text/css'
    return scss.parser.load('style.scss')


@bottle.route('/<path:path>')
@bottle.route('/')
def reviews(path=False):
    review_file = open('reviews.json')
    reviews = json.load(review_file)['reviews']
    review_file.close()

    types = set()

    for review in reviews:
        typeslug = slugify(review['type']) + 's'
        types.add((review['type'], typeslug))
        review['slug'] = slugify(review['title'])
        review['typeslug'] = typeslug

        if 'words' in review:
            words = []
            for word in review['words']:
                if word.islower():
                    word = word.capitalize()

                words.append('<span class="word">%s.</span>' % word)

            review['words_string'] = ' '.join(words)

    return bottle.template('reviews', reviews=reviews, types=types)

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8081)
    #from flup.server.fcgi import WSGIServer
    #WSGIServer(application).run()
