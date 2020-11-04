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

from typing import TYPE_CHECKING

from rdflib import RDF

from oc_ocdm.decorators import accepts_only

if TYPE_CHECKING:
    from typing import Optional, List
    from rdflib import URIRef
    from oc_ocdm.entities.bibliographic import ReferencePointer
    from oc_ocdm.entities.bibliographic import PointerList
from oc_ocdm import GraphEntity
from oc_ocdm.entities import BibliographicEntity


class DiscourseElement(BibliographicEntity):
    """Discourse element (short: de): a document component, either structural (e.g.
       paragraph, section, chapter, table, caption, footnote, title) or rhetorical (e.g.
       introduction, discussion, acknowledgements, reference list, figure, appendix), in which
       the content of a bibliographic resource can be organized."""

    # HAS TITLE
    def get_title(self) -> Optional[str]:
        return self._get_literal(GraphEntity.iri_title)

    @accepts_only('literal')
    def has_title(self, string: str) -> None:
        """The title of the discourse element, such as the title of a figure or a section in an article.
        """
        self.remove_title()
        self._create_literal(GraphEntity.iri_title, string)

    def remove_title(self) -> None:
        self.g.remove((self.res, GraphEntity.iri_title, None))
    
    # HAS PART (DiscourseElement)
    def get_discourse_elements(self) -> List[DiscourseElement]:
        uri_list: List[URIRef] = self._get_multiple_uri_references(GraphEntity.iri_contains_de)
        result: List[DiscourseElement] = []
        for uri in uri_list:
            result.append(self.g_set.add_de(self.resp_agent, self.source_agent, self.source, uri))
        return result

    @accepts_only('de')
    def contains_discourse_element(self, de_res: DiscourseElement) -> None:
        """The discourse element hierarchically nested within the parent element, such as a
        sentence within a paragraph, or a paragraph within a section.
        """
        self.g.add((self.res, GraphEntity.iri_contains_de, de_res.res))

    @accepts_only('de')
    def remove_contained_de(self, de_res: DiscourseElement = None) -> None:
        if de_res is not None:
            self.g.remove((self.res, GraphEntity.iri_contains_de, de_res.res))
        else:
            self.g.remove((self.res, GraphEntity.iri_contains_de, None))

    # HAS NEXT (DiscourseElement)
    def get_next_de(self) -> Optional[DiscourseElement]:
        uri: Optional[URIRef] = self._get_uri_reference(GraphEntity.iri_has_next)
        if uri is not None:
            return self.g_set.add_de(self.resp_agent, self.source_agent, self.source, uri)

    @accepts_only('de')
    def has_next_de(self, de_res: DiscourseElement) -> None:
        """The following discourse element that includes at least one in-text reference pointer.
        """
        self.remove_next_de()
        self.g.add((self.res, GraphEntity.iri_has_next, de_res.res))

    def remove_next_de(self) -> None:
        self.g.remove((self.res, GraphEntity.iri_has_next, None))

    # IS CONTEXT OF (ReferencePointer)
    def get_context_of_rp(self) -> List[ReferencePointer]:
        uri_list: List[URIRef] = self._get_multiple_uri_references(GraphEntity.iri_is_context_of)
        result: List[ReferencePointer] = []
        for uri in uri_list:
            result.append(self.g_set.add_rp(self.resp_agent, self.source_agent, self.source, uri))
        return result

    @accepts_only('rp')
    def is_context_of_rp(self, rp_res: ReferencePointer) -> None:
        """Provides the textual and semantic context of the in-text reference pointer
        that appears within the discourse element.
        """
        self.g.add((self.res, GraphEntity.iri_is_context_of, rp_res.res))

    @accepts_only('rp')
    def remove_context_of_rp(self, rp_res: ReferencePointer = None) -> None:
        if rp_res is not None:
            self.g.remove((self.res, GraphEntity.iri_is_context_of, rp_res.res))
        else:
            self.g.remove((self.res, GraphEntity.iri_is_context_of, None))

    # IS CONTEXT OF (PointerList)
    def get_context_of_pl(self) -> List[PointerList]:
        uri_list: List[URIRef] = self._get_multiple_uri_references(GraphEntity.iri_is_context_of)
        result: List[PointerList] = []
        for uri in uri_list:
            result.append(self.g_set.add_pl(self.resp_agent, self.source_agent, self.source, uri))
        return result

    @accepts_only('pl')
    def is_context_of_pl(self, pl_res: PointerList) -> None:
        """Provides the textual and semantic context of the list of
        in-text reference pointers that appears within the discourse element.
        """
        self.g.add((self.res, GraphEntity.iri_is_context_of, pl_res.res))

    @accepts_only('pl')
    def remove_context_of_pl(self, pl_res: PointerList = None) -> None:
        if pl_res is not None:
            self.g.remove((self.res, GraphEntity.iri_is_context_of, pl_res.res))
        else:
            self.g.remove((self.res, GraphEntity.iri_is_context_of, None))

    # HAS CONTENT
    def get_content(self) -> Optional[str]:
        return self._get_literal(GraphEntity.iri_has_content)

    @accepts_only('literal')
    def has_content(self, string: str) -> None:
        """The literal document text contained by the discourse element.
        """
        self.remove_content()
        self._create_literal(GraphEntity.iri_has_content, string)

    def remove_content(self) -> None:
        self.g.remove((self.res, GraphEntity.iri_has_content, None))

    # HAS NUMBER
    def get_number(self) -> Optional[str]:
        return self._get_literal(GraphEntity.iri_has_sequence_identifier)

    @accepts_only('literal')
    def has_number(self, string: str) -> None:
        self.remove_number()
        self._create_literal(GraphEntity.iri_has_sequence_identifier, string)

    def remove_number(self) -> None:
        self.g.remove((self.res, GraphEntity.iri_has_sequence_identifier, None))

    # HAS TYPE
    def get_types(self) -> List[URIRef]:
        uri_list: List[URIRef] = self._get_multiple_uri_references(RDF.type)
        return uri_list

    @accepts_only('thing')
    def create_discourse_element(self, de_class: URIRef) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        if de_class is not None:
            self._create_type(de_class)
        else:
            self._create_type(GraphEntity.iri_discourse_element)

    def create_section(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_section)

    def create_section_title(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_section_title)

    def create_paragraph(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_paragraph)

    def create_sentence(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_sentence)

    def create_text_chunk(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_text_chunk)

    def create_table(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_table)

    def create_footnote(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_footnote)

    def create_caption(self) -> None:
        """The type of discourse element – such as “paragraph”, “section”, “sentence”,
        “acknowledgements”, “reference list” or “figure”.
        """
        self._create_type(GraphEntity.iri_caption)

    @accepts_only('thing')
    def remove_type(self, type_ref: URIRef = None) -> None:
        if type_ref is not None:
            self.g.remove((self.res, RDF.type, type_ref))
        else:
            self.g.remove((self.res, RDF.type, None))
