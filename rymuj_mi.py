#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import random
import sys

NN = 10 * 1000
MAX = 120
CONSONANTS = 'bcćdfghjklłmnńpqrsśtvwxzźż'

PREFIXES = [
    'bez', 'naj', 'nie',
    'do', 'nade', 'nad', 'na', 'obe', 'ob', 'ode', 'od', 'o',
    'pode', 'pod', 'po', 'prze', 'przy', 'roze', 'roz', 's', 'ś',
    'u', 'we', 'ws', 'wy', 'wze', 'wz', 'w', 'za', 'ze', 'z',
    'pięć', 'sześć', 'siedem', 'siedm', 'osiem', 'ośm', 'dziewięć',
    'dwu', 'trzy', 'cztero', 'pięcio', 'sześcio', 'siedmio', 'ośmio',
    'dwój', 'trój', 'czwór',
    'jede', 'czter', 'pięt', 'szes', 'dziewięt',
    'obu', 'kilka', 'kilku', 'pół', 'spół', 'współ',
    'ma', 'twa', 'swa',
    'mą', 'twą', 'swą',
    'me', 'twe', 'swe',
    'mo', 'two', 'swo',
    'mój', 'twój', 'swój',
    'mym', 'twym', 'swym',
    'nas', 'was',
    'ciebi', 'siebi', 'tobi', 'sobi',
    'mało', 'wielo', 'jasno', 'ciemno', 'równo', 'różno',
    'arcy', 'eks', 'krypto',
]


def ClearNonFeminine(d):
  d.pop('XXX0', None)
  d.pop('XXX1', None)
  d.pop('XXX3', None)
  d.pop('XXX4', None)


def Normalize(w):
  w = w.rsplit('_', 1)[-1]
  w = w.rstrip(CONSONANTS)
  if w[-2:] == 'ą':
    w = w[:-2] + 'o'
  elif w[-2:] == 'ę':
    w = w[:-2] + 'e'
  return w


def IsTrivial(a, b):
  a = Normalize(a)
  b = Normalize(b)
  if a == b:
    return True
  codas = set([a])
  for prefix in PREFIXES:
    if a.startswith(prefix):
      codas.add(a[len(prefix):])
    if b.startswith(prefix):
      bb = b[len(prefix):]
      if bb in codas:
        return True
  if b in codas:
    return True
  return False


def AnyIsTrivial(w, words):
  for word in words:
    if IsTrivial(w[1], word[1]):
      return True
  return False


def CountAll(words):
  d = collections.defaultdict(list)
  for r, w in words:
    d[r.lstrip('0').rstrip(CONSONANTS)].append(w)
  ClearNonFeminine(d)
  total = 0
  for r in d.itervalues():
    total += (len(r) * (len(r) - 1)) // 2
  return total


def CountNonGrammatical(words):
  d = collections.defaultdict(list)
  for r, _ in words:
    d[r.lstrip('0').rstrip(CONSONANTS)].append(r)
  ClearNonFeminine(d)
  total = 0
  for r in d.itervalues():
    l = len(r)
    if l >= 2:
      sub = sum(x[0].startswith('0') for x in r)
      if sub > 1:
        l -= (sub - 1)
      total += (l * (l - 1)) // 2
  return total


def CountExact(words):
  d = collections.defaultdict(list)
  for r, _ in words:
    d[r.lstrip('0')].append(r)
  ClearNonFeminine(d)
  total = 0
  for r in d.itervalues():
    l = len(r)
    if l >= 2:
      sub = sum(x[0].startswith('0') for x in r)
      if sub > 1:
        l -= (sub - 1)
      total += (l * (l - 1)) // 2
  return total


def CountTriple(words):
  d = collections.defaultdict(list)
  for r, w in words:
    d[r.lstrip('0').rstrip(CONSONANTS)].append(w)
  ClearNonFeminine(d)
  total = 0
  for r in d.itervalues():
    total += (len(r) * (len(r) - 1) * (len(r) - 2)) // 6
  return total


def main():
  words = []
  with open(sys.argv[1]) as f:
    for line in f:
      words.append(line.split())
  for i in xrange(2, MAX + 1):
    all = 0.0
    nongrammatical = 0.0
    exact = 0.0
    triple = 0.0
    for _ in xrange(NN):
      selected = set()
      while len(selected) < i:
        added = random.choice(words)
        added = (added[0], added[1].rsplit('_')[-1])
        selected.add(added)
      all += CountAll(selected)
      nongrammatical += CountNonGrammatical(selected)
      exact += CountExact(selected)
      triple += CountTriple(selected)
    s = '%s %s %s %s %s\n' % (i, all / NN, nongrammatical / NN, exact / NN, triple / NN)
    sys.stdout.write(s)
    sys.stderr.write(s)


if __name__ == '__main__':
  main()
