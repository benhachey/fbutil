#!/usr/bin/env python2.7
"""
Script to extract names and aliases from Freebase RDF dump.
"""
import gzip
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

def read_mids(f):
    log.info('Reading mids..')
    mids = frozenset([m.strip() for m in gzip.open(f, 'rb').readlines()])
    log.info('..done (%d).' % len(mids))
    return mids

def mid(s):
    s = s.strip('<>')
    if s.startswith('http://rdf.freebase.com/ns/m.'):
        return s[27:]

def main(dumpf, midsf, namef, aliasf):
    mid_set = read_mids(midsf)
    name_fh = open(namef, 'w')
    alias_fh = open(aliasf, 'w')
    log.info('Scanning dump for names/aliases..')
    for i, line in enumerate(gzip.open(dumpf, 'rb')):
        if i % 1000000 == 0:
            log.info('..%d..' % i)
        fields = line.strip().split('\t')
        if len(fields) != 4:
            log.warn('Unexpected format: %s' % line)
        s, p, o, t = fields
        if mid(s) in mid_set:
            p = p.strip('<>')
            if p.endswith('type.object.name'):
                name_fh.write(line)
            elif p.endswith('common.topic.alias'):
                alias_fh.write(line)
    log.info('..done.')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Extract names/aliases from FB')
    p.add_argument('dump', help='Path to Freebase RDF dump file')
    p.add_argument('mids', help='List of MIDs to extract')
    p.add_argument('names', help='Output file for names')
    p.add_argument('aliases', help='Output file for aliases')
    args = p.parse_args()
    main(args.dump, args.mids, args.names, args.aliases)

