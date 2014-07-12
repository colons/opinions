#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import json
import re
import sys

root = os.path.dirname(os.path.realpath(__file__))

sys.path.append(root)
os.chdir(root)

import bottle
from django.template.defaultfilters import slugify
import scss.parser


def parse_path(path):
    filters = []
    filter_repl = {
        'type': 'typeslug',
    }

    if path is not None:
        for section in path.split('/'):
            if not section:
                continue

            matches = re.findall(r'^([^=]+)=([^=]+)$', section)

            if matches:
                filters.append({filter_repl.get(matches[0][0], matches[0][0]):
                                matches[0][1]})
            else:
                filters.append({'slug': section})

    return filters


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
def reviews(path=None):
    review_file = open('reviews.json')
    reviews = json.load(review_file)['reviews']
    review_file.close()

    types = set()

    filters = parse_path(path)

    for review in reviews:
        review['active'] = True

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

        for a_filter in filters:
            for key, value in a_filter.iteritems():
                if key not in review or unicode(review[key]) != value:
                    review['active'] = False

    return bottle.template('reviews', reviews=reviews, types=types)


application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8081)
    # from flup.server.fcgi import WSGIServer
    # WSGIServer(application).run()
