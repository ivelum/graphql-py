import re
from unittest import TestCase

from graphql.parser import GraphQLParser
from graphql.exceptions import SyntaxError


class GraphQLParseTest(TestCase):
    parser = GraphQLParser()

    def assert_parse(self, ast, expected):
        expected = re.sub(r'[\n ]+', '', expected)
        self.assertEqual(expected, repr(ast).replace(' ', ''))

    def test_shorthand(self):
        self.assert_parse(
            self.parser.parse('{ me { name } }'),
            """
            <Document: definitions=[
                <Query: selections=[
                    <Field: selections=[<Field:name=name>], name=me>
                ]>
            ]>
            """
        )
        self.assert_parse(
            self.parser.parse("""
                {
                  user(id: 4) {
                    id
                    name
                    profilePic
                    avatar: profilePic(width: 30, height: 30)
                  }
                }
            """),
            """
            <Document: definitions=[
                <Query: selections=[
                    <Field:
                        selections=[
                            <Field: name=id>,
                            <Field: name=name>,
                            <Field: name=profilePic>,
                            <Field: alias=avatar, name=profilePic, arguments=[
                                <Argument: name=width, value=30>,
                                <Argument: name=height, value=30>
                            ]>
                        ],
                        name=user,
                        arguments=[<Argument: name=id, value=4>]>
                ]>
            ]>
            """,
        )

    def test_with_fragments(self):
        self.assert_parse(
            self.parser.parse("""
                query withNestedFragments {
                  user(id: 4) {
                    friends(first: 10) {
                      ...friendFields
                    }
                    mutualFriends(first: 10) {
                      ...friendFields
                    }
                  }
                }

                fragment friendFields on User {
                  id
                  name
                  ...standardProfilePic
                }

                fragment standardProfilePic on User {
                  profilePic(size: 50)
                }
            """),
            """
            <Document: definitions=[
                <Query: name=withNestedFragments,
                    selections=[
                        <Field: selections=[
                            <Field: selections=[
                                    <FragmentSpread: name=friendFields>
                                ],
                                name=friends,
                                arguments=[
                                    <Argument: name=first, value=10>
                                ]>,
                            <Field: selections=[
                                    <FragmentSpread: name=friendFields>
                                ],
                                name=mutualFriends,
                                arguments=[
                                    <Argument: name=first, value=10>
                                ]>
                        ],
                        name=user,
                        arguments=[<Argument:name=id,value=4>]>
                    ]
                >,
                <FragmentDefinition:
                    type_condition=<NamedType: name=User>,
                    name=friendFields,
                    selections=[
                        <Field:name=id>,
                        <Field:name=name>,
                        <FragmentSpread: name=standardProfilePic>
                    ]
                >,
                <FragmentDefinition:
                    type_condition=<NamedType:name=User>,
                    name=standardProfilePic,
                    selections=[
                        <Field: name=profilePic,
                            arguments=[<Argument:name=size,value=50>]
                        >
                ]>
            ]>

            """
        )
