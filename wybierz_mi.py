#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import re
import rym

N_WORDS = 1000

FAKE_PROCLITICS = set("""
  a aż bo choć co czy gdy gdyż i iż jak lecz lub niż zaś że żem żeś
  le la les de du del des al au the of der die das
""".split())

ENCLITICS = set("""
  em eś li no się se to
  mię mnie mi mną ci cię mu go nim jej ją nią
  my nas nam wy was wam ich im
""".split())

GRAMMATICAL_RHYME = re.compile(
    '(ami|ego|emu|owi|owie|ejsz(a|ą|e|ej|y|ych|ym)|ejsi|[iy]mi|'
    'ośc(i|iach|ią|iom)|[aeiy](cie|my)|[aeu](ją|jąc|jcie|je|jesz|ję|jmy)|'
    '(a|ę|i|y)li|(a|e|ę|i|y)(ła|łam|łaś|łem|łeś|ło|ły)|(a|ą|i|y)wszy|'
    '(an|ąc|ęt|on|ow)(a|ą|e|ej|o|y|ych|ym)|'
    '(an|en|ęc|ic|yc)(i|ia|iach|iam|ie|iem|iu)|[oiy](wać|wał)|kolwiek|nastu|'
    '^(m|tw|sw)o(ja|ją|je|jej|i|ich|im)|^[nw]as(za|zą|ze|zej|i|zych|zym))$')

BASE_32_TABLE = [
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
  +0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -1, -1, -1, -1, -1,
  -1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
  25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, -1, -1, -1, -1, -1,
  -1, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
  51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
]


def ReadWords():
  words = []
  with open('zestroje.d') as f:
    for line in f:
      words.append(line.split()[0])
  repeated = []
  with open('model.d') as f:
    for n, line in enumerate(f):
      i = 0
      num = -1
      while i < len(line):
        while True:
          d = BASE_32_TABLE[ord(line[i])]
          i += 1
          if d < 0:
            break
          if d >= 32:
            break
        num += 1
      if n > 1:
        for _ in xrange(num):
          repeated.append(words[n])
  return repeated


def ToLower(word):
  return unicode(
      unicode(word, 'utf-8').encode('iso-8859-2').lower(),
      'iso-8859-2').encode('utf-8')


def main():
  repeated = ReadWords()
  selected = []
  while len(selected) < N_WORDS:
    word = random.choice(repeated)
    split_word = word.split('_')
    if split_word[-1] in ENCLITICS:
      continue
    while len(split_word) > 1 and split_word[0] in FAKE_PROCLITICS:
      split_word = split_word[1:]
    normalized_word = ToLower(''.join(split_word))
    _, rhyme = rym.GetLengthAndRhyme(normalized_word)
    length, _ = rym.GetLengthAndRhyme(rhyme)
    if length != 2:
      rhyme = 'XXX%d' % length
    elif GRAMMATICAL_RHYME.search(normalized_word):
      rhyme = '0' + rhyme
    selected.append((rhyme, word))
  selected.sort()
  for word in selected:
    print word[0], word[1]


if __name__ == '__main__':
  main()
