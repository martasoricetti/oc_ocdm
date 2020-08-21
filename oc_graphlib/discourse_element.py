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

from typing import Union

from rdflib import URIRef

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from oc_graphlib.reference_pointer import ReferencePointer
from oc_graphlib.graph_entity import GraphEntity
from oc_graphlib.bibliographic_entity import BibliographicEntity

"""
Notes about DE:

    HAS TYPE is generated by the factory methods!
    HAS PART (DiscourseElement) has both direct and inverted logic implemented! Have a look below for more info.
    Chill down, everything seems OK here!
"""


class DiscourseElement(BibliographicEntity):
    # HAS TITLE
    # <self.res> DCTERMS:title "string"
    def create_title(self, string: str) -> bool:
        return self._create_literal(GraphEntity.title, string)

    # HAS PART (DiscourseElement)
    # <self.res> FRBR:part <de_res>
    def contains_discourse_element(self, de_res: DiscourseElement) -> None:  #  new
        self.g.add((self.res, GraphEntity.contains_de, URIRef(str(de_res))))

    """
         HAS PART (DiscourseElement) with inverted logic (IS PART OF)
    """
    # <de_res> FRBR:part <self.res>
    def contained_in_discourse_element(self, de_res: DiscourseElement) -> None:  #  new
        self.g.add((URIRef(str(de_res)), GraphEntity.contains_de, self.res))

    # HAS NEXT (DiscourseElement)
    # <self.res> OCO:hasNext <de_res>
    def has_next_de(self, de_res: DiscourseElement) -> None:  # new
        self.g.add((self.res, GraphEntity.has_next, URIRef(str(de_res))))

    # IS CONTEXT OF (ReferencePointer or PointerList)
    # <self.res> C4O:isContextOf <de_res>
    # TODO: Invece di usare typings.Union si potrebbero creare due metodi diversi
    #       (uno per DiscourseElement e uno per ReferencePointer), ovvero is_context_of_rp e is_context_of_de
    def is_context_of_rp_or_pl(self, de_res: Union[DiscourseElement, ReferencePointer]) -> None:
        self.g.add((self.res, GraphEntity.is_context_of, URIRef(str(de_res))))

    # HAS CONTENT
    # <self.res> C4O:hasContent "string"
    def create_content(self, string: str) -> bool:
        return self._create_literal(GraphEntity.has_content, string)

    # ++++++++++++++++++++++++ FACTORY METHODS ++++++++++++++++++++++++
    # <self.res> RDF:type <type>

    def create_discourse_element(self, de_class: URIRef) -> None:  #  new
        if de_class is not None:
            self._create_type(de_class)
        else:
            self._create_type(GraphEntity.discourse_element)

    def create_section(self) -> None:
        self._create_type(GraphEntity.section)

    # missing SectionTitle (DOCO:SectionTitle)
    # missing Paragraph (DOCO:Paragraph)

    def create_sentence(self) -> None:  #  new
        self._create_type(GraphEntity.sentence)

    def create_text_chunk(self) -> None:  #  new
        self._create_type(GraphEntity.text_chunk)

    # missing Table (DOCO:Table)
    # missing Footnote (DOCO:Footnote)
    # missing Caption (DEO:Caption)
