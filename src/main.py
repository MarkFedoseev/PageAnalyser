from bs4 import BeautifulSoup
import bs4
import random
import matplotlib.pyplot as plt
import os

import json

import sys
import argparse
import threading

from yaml import parse

from block import Block
from block import CharacteristicBlock
from structure_organiser import StructureOrganiser

argparser = argparse.ArgumentParser()
argparser.add_argument('--page', help='imported page or folder', default='')
args = argparser.parse_args()

parsed_page = None
parsed_pages = None
if args.page != '':
    PagePath = args.page
    with open(PagePath, encoding='utf-8') as file:
        try:
            parsed_page = BeautifulSoup(file, 'html.parser')
        except:
            print('selected file is not an html page')
            print('exiting..')
            exit()
else:
    parsed_page = BeautifulSoup(input(), 'html.parser')


if not os.path.exists('./result'):
    os.mkdir('./result')
if not os.path.exists('./result/pics'):
    os.mkdir('./result/pics')


#dict of configs
Config = None
with open('config.json', 'r') as file:
    Config = json.load(file)



def init_StructureOrganiser(config):
    structureOrganiser = StructureOrganiser()
    structureOrganiser.add_tagsvector(StructureOrganiser.TagsVector(
            config['tags']['block'] + config['tags']['inline'],
            config['tags']['block'],
            config['tags']['inline'])
        )
    return structureOrganiser






#dict of all blocks in page
structureOrganiser = init_StructureOrganiser(Config)

#args: {Blocks dict, page, }
def CreateBlock(block, args):
    args['Blocks'].update({hash(block.me) : block})
    if isinstance(block.me, bs4.element.Tag):
        for blk in block.me.children:
            if isinstance(blk, bs4.element.Tag) and blk.children != None:
                #args['Blocks'].update({hash(blk) : Block(blk, args['Page'], args['Blocks'][hash(block.me)], CreateBlock, args)})
                Block(blk, args['Page'], args['Blocks'][hash(block.me)], CreateBlock, args)
                block.children.append(args['Blocks'][hash(blk)])

Blocks = {}
Block(parsed_page.body, parsed_page, None, CreateBlock, {'Blocks' : Blocks, 'Page' : parsed_page})

for block in Blocks.values():
    block.add_characteristic(structureOrganiser)

print(len(Blocks))


for block in Blocks.values():
    block.add_characteristic(structureOrganiser)

def find_similar(Blocks):
    sims = []
    _Blocks = Blocks.copy()

    def similars(_Blocks, lst):
        key, block = random.choice(list(_Blocks.items()))
        sims = block.characteristic.get_similars(_Blocks)[1]
        if sims == [key]:
            _Blocks.pop(key)
        else:
            lst.append(sims)
            for sim in lst[-1]:
                _Blocks.pop(sim)
        if len(_Blocks) != 0:
            similars(_Blocks, lst)

    similars(_Blocks, sims)

    similars_str = ''
    for sim in sims:
        similars_str += str(sim) + '\n'
    with open('./result/similars.txt', 'w') as file:
        file.write(similars_str)

def find_similar_structures(Blocks):
    sims = []
    _Blocks = Blocks.copy()
    def similars_structure(_Blocks, lst):
        key, block = random.choice(list(_Blocks.items()))
        sims = block.characteristic.get_similars_structure(_Blocks)
        if sims == [key]:
            _Blocks.pop(key)
        else:
            lst.append(sims)
            for sim in lst[-1]:
                _Blocks.pop(sim)
        if len(_Blocks) != 0:
            similars_structure(_Blocks, lst)

    similars_structure(_Blocks, sims)

    sims_source = []
    for sim in sims:
        sims_source.append([(Blocks[s].me.sourceline, Blocks[s].me.sourcepos) for s in sim])
    similars_structure_str = ''
    for sim in sims_source:
        similars_structure_str += str(sim) + '\n'
    with open('./result/similar_structures.txt', 'w') as file:
        file.write(similars_structure_str)

def graph_body(parsed_page, Blocks):
    body = parsed_page.body
    bodyBlock = Blocks[hash(body)]
    bodyBlock.characteristic.graph(plt, Config, 'all')
    graph_names = [
        'firstorder_block', 'firstorder_inline', 'firstorder_all',
        'full_block', 'full_inline', 'full_all'
        ]
    for i in plt.get_fignums():
        plt.figure(i).savefig(f'./result/pics/{graph_names[i - 1]}')

find_similar(Blocks)
find_similar_structures(Blocks)
graph_body(parsed_page, Blocks)

def ComparePages(pages, Config, structureOrganiser):
    Bodies = {}
    for page in pages:
        Bodies.update({hash(page.body) : Block(page.body, page, None)})
    for body in Bodies:
        body.add_characteristic(structureOrganiser)
    