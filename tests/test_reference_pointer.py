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

from rdflib import Literal

from oc_ocdm import GraphEntity
from oc_ocdm import GraphSet
from oc_ocdm.counter_handler import FilesystemCounterHandler


class TestReferencePointer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.counter_handler = FilesystemCounterHandler("./info_dir/")
        cls.graph_set = GraphSet("http://test/", "context_base", cls.counter_handler, "", wanted_label=False)

    def setUp(self):
        self.graph_set.g = []
        self.an = self.graph_set.add_an(self.__class__.__name__)
        self.rp1 = self.graph_set.add_rp(self.__class__.__name__)
        self.rp2 = self.graph_set.add_rp(self.__class__.__name__)
        self.be = self.graph_set.add_be(self.__class__.__name__)

    def test_has_content(self):
        content = "Content"
        result = self.rp1.has_content(content)
        self.assertIsNone(result)

        triple = self.rp1.res, GraphEntity.iri_has_content, Literal(content)
        self.assertIn(triple, self.rp1.g)

    def test_has_next_rp(self):
        result = self.rp1.has_next_rp(self.rp2)
        self.assertIsNone(result)

        triple = self.rp1.res, GraphEntity.iri_has_next, self.rp2.res
        self.assertIn(triple, self.rp1.g)

    def test_denotes_be(self):
        result = self.rp1.denotes_be(self.be)
        self.assertIsNone(result)

        triple = self.rp1.res, GraphEntity.iri_denotes, self.be.res
        self.assertIn(triple, self.rp1.g)

    def test_has_annotation(self):
        result = self.rp1.has_annotation(self.an)
        self.assertIsNone(result)

        triple = self.rp1.res, GraphEntity.iri_has_annotation, self.an.res
        self.assertIn(triple, self.rp1.g)


if __name__ == '__main__':
    unittest.main()
