#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2016, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
from __future__ import annotations
import re

from rdflib import URIRef

from oc_graphlib.prov_entity import GraphEntity
from oc_graphlib.support.support import is_string_empty, encode_url

"""
Notes about ID:

    HAS LITERAL VALUE and HAS SCHEME are generated by factory methods!
    Chill down, everything seems OK here!
"""


class Identifier(GraphEntity):
    # ++++++++++++++++++++++++ FACTORY METHODS ++++++++++++++++++++++++
    def create_orcid(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(string, GraphEntity.orcid)

    def create_doi(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(string.lower(), GraphEntity.doi)

    def create_pmid(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(string, GraphEntity.pmid)

    def create_pmcid(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(string, GraphEntity.pmcid)

    def create_issn(self, string: str) -> bool:
        cur_string = re.sub("–", "-", string)
        if cur_string != "0000-0000":
            return self._associate_identifier_with_scheme(string, GraphEntity.issn)

    def create_isbn(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(
            re.sub("–", "-", string), GraphEntity.isbn)

    def create_url(self, string: str) -> bool:
        return self._associate_identifier_with_scheme(encode_url(string.lower()), GraphEntity.url)

    def create_xpath(self, string: str) -> bool:  #  new
        return self._associate_identifier_with_scheme(string, GraphEntity.xpath)

    def create_intrepid(self, string: str) -> bool:  #  new
        return self._associate_identifier_with_scheme(string, GraphEntity.intrepid)

    def create_xmlid(self, string: str) -> bool:  #  new
        return self._associate_identifier_with_scheme(string, GraphEntity.xmlid)

    def create_wikidata(self, string: str) -> bool:  # new
        return self._associate_identifier_with_scheme(string, GraphEntity.wikidata)

    def create_crossref(self, string: str) -> bool:  # new
        return self._associate_identifier_with_scheme(string, GraphEntity.crossref)

    def create_viaf(self, string: str) -> bool:  # new
        return self._associate_identifier_with_scheme(string, GraphEntity.viaf)

    # <self.res> LITERAL:hasLiteralValue "string"
    # <self.res> DATACITE:usesIdentifierScheme <id_type>
    def _associate_identifier_with_scheme(self, string: str, id_type: URIRef) -> bool:
        if not is_string_empty(string):
            self._create_literal(GraphEntity.has_literal_value, string)
            self.g.add((self.res, GraphEntity.uses_identifier_scheme, id_type))
            return True
        return False
