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
import unittest

from rdflib import URIRef

from oc_ocdm.graph_entity import GraphEntity
from oc_ocdm.graph_set import GraphSet
from oc_ocdm.counter_handler.filesystem_counter_handler import FilesystemCounterHandler


class TestReferenceAnnotation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.counter_handler = FilesystemCounterHandler("./info_dir/")
        cls.graph_set = GraphSet("http://test/", "context_base", cls.counter_handler, 0, "", wanted_label=False)

    def setUp(self):
        self.graph_set.g = []
        self.an = self.graph_set.add_an(self.__class__.__name__)
        self.br1 = self.graph_set.add_br(self.__class__.__name__)
        self.br2 = self.graph_set.add_br(self.__class__.__name__)
        self.ci = self.graph_set.add_ci(self.__class__.__name__, self.br1, self.br2)

    def test_create_body_annotation(self):
        result = self.an._create_body_annotation(self.ci)
        self.assertIsNone(result)

        triple = URIRef(str(self.an)), GraphEntity.has_body, URIRef(str(self.ci))
        self.assertIn(triple, self.an.g)


if __name__ == '__main__':
    unittest.main()
