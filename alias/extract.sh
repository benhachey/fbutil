#!/usr/bin/env bash
#
# Script to extract names and aliases from Freebase RDF dump

DUMP=/data/freebase/freebase-rdf-2013-12-01-00-00 # SETME

FN=`echo $DUMP | sed 's/.*\///'`

ENWP=$FN.enwp
gunzip -c $DUMP.gz \
    | grep "en\.wikipedia\.org" \
    | grep -v "curid=" \
    > $ENWP
gzip $ENWP

MIDS=$FN.enwp.mids
gunzip -c $ENWP.gz \
    | sed 's/^<http\:\/\/rdf\.freebase\.com\/ns\/\(m\.[^>]*\)>.*/\1/' \
    > $MIDS
gzip $MIDS

NAMES=$FN.enwp.names
ALIASES=$FN.enwp.aliases
python extract.py \
    $DUMP.gz \
    $MIDS.gz \
    $NAMES \
    $ALIASES
gzip $NAMES
gzip $ALIASES

gunzip -c $NAMES.gz \
    | cut -f1,3 \
    | sed 's/<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    > $NAMES.terse
gzip $NAMES.terse

gunzip -c $ALIASES.gz \
    | cut -f1,3 \
    | sed 's/<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    > $ALIASES.terse
gzip $ALIASES.terse

gunzip -c $ENWP.gz \
    | cut -f1,3 \
    | sed 's/^<http\:\/\/rdf\.freebase\.com\/ns\/\([^>]*\)>/\1/' \
    | sed 's/<http\:\/\/en\.wikipedia\.org\/wiki\/\([^>]*\)>$/\1/' \
    > $ENWP.terse
gzip $ENWP.terse
