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

from oc_graphlib.graph_entity import GraphEntity
from oc_graphlib.bibliographic_entity import BibliographicEntity

"""
Notes about RE:

    HAS TYPE is missing! (Maybe factory methods are missing too)
    HAS FORMAT is missing!
    HAS URL is missing!
"""


class ResourceEmbodiment(BibliographicEntity):
    # HAS FIRST PAGE
    # <self.res> PRISM:startingPage "string"
    def create_starting_page(self, string: str) -> bool:
        if re.search("[-–]+", string) is None:
            page_number = string
        else:
            page_number = re.sub("[-–]+.*$", "", string)
        return self._create_literal(GraphEntity.starting_page, page_number)

    # HAS LAST PAGE
    # <self.res> PRISM:endingPage "string"
    def create_ending_page(self, string: str) -> bool:
        if re.search("[-–]+", string) is None:
            page_number = string
        else:
            page_number = re.sub("^.*[-–]+", "", string)
        return self._create_literal(GraphEntity.ending_page, page_number)

    # ++++++++++++++++++++++++ FACTORY METHODS ++++++++++++++++++++++++
    # <self.res> RDF:type <type>

    def create_digital_embodiment(self) -> None:
        self._create_type(GraphEntity.digital_manifestation)

    # missing Digital embodiment (FABIO:DigitalManifestation)
    # missing Print embodiment (FABIO:PrintObject)
