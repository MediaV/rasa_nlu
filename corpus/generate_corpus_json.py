#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import json

def read_corpus(filename):
    corpus = []
    with open(filename) as f:
        intent = f.readline()[:-1]
        for line in f.xreadlines():
            parts = line[:-1].split()
            text = parts[0]
            slots = {}
            for v in parts[1:]:
                slot_name, slot_value = v.split(':')
                slots[slot_name] = slot_value
            corpus.append((intent, text, slots))
    return corpus

def gen_corpus_dict(corpus):
    common_examples = []
    for intent, text, slots in corpus:
        entities = []
        for k, v in slots.iteritems():
            unicode_text = text.decode('utf-8')
            unicode_v = v.decode('utf-8')
            entity = {}
            entity['start'] = unicode_text.find(unicode_v)
            entity['end'] = entity['start'] + len(unicode_v)
            entity['value'] = v
            entity['entity'] = k
            entities.append(entity)
        common_examples.append({'text': text, 'intent': intent, 'entities': entities})
    d = {}
    d['rasa_nlu_data'] = {}
    d['rasa_nlu_data']['common_examples'] = common_examples
    return d

if __name__ == '__main__':
    filename = sys.argv[1]
    corpus = read_corpus(filename)
    corpus_dict = gen_corpus_dict(corpus)
    print json.dumps(corpus_dict, indent=2, ensure_ascii=False)
