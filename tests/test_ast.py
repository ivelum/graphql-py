from unittest import TestCase

from graphql.ast import Document, Query, Mutation, Field


class GraphQLASTTest(TestCase):
    def test_equality(self):
        self.assertEqual(Document(), Document())
        doc1 = Document(definitions=[
            Query(selections=[Field(name='me')], name='q'),
        ])
        self.assertEqual(
            doc1,
            Document(definitions=[
                Query(selections=[Field(name='me')], name='q')
            ]),
        )
        self.assertNotEqual(
            doc1,
            Document(definitions=[
                Query(selections=[Field(name='not_me')], name='q')
            ]),
        )
        self.assertNotEqual(
            doc1,
            Document(definitions=[
                Mutation(selections=[Field(name='me')], name='q')
            ]),
        )
