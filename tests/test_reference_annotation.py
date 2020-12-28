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

from oc_ocdm.graph import GraphEntity
from oc_ocdm.graph import GraphSet
from oc_ocdm.counter_handler import FilesystemCounterHandler


class TestReferenceAnnotation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.counter_handler = FilesystemCounterHandler("./info_dir/")
        cls.graph_set = GraphSet("http://test/", cls.counter_handler, "", False)

    def setUp(self):
        self.an = self.graph_set.add_an(self.__class__.__name__)
        self.br1 = self.graph_set.add_br(self.__class__.__name__)
        self.br2 = self.graph_set.add_br(self.__class__.__name__)
        self.ci = self.graph_set.add_ci(self.__class__.__name__)

    def test_has_body_annotation(self):
        result = self.an.has_body_annotation(self.ci)
        self.assertIsNone(result)

        triple = self.an.res, GraphEntity.iri_has_body, self.ci.res
        self.assertIn(triple, self.an.g)


if __name__ == '__main__':
    unittest.main()
