from unittest import TestCase

from graphql.ast import Document, Query, Field, Argument, FragmentDefinition, \
    FragmentSpread, NamedType, Variable, VariableDefinition, Subscription, NonNullType
from graphql.parser import GraphQLParser


class GraphQLParseTest(TestCase):
    parser = GraphQLParser()

    def test_shorthand(self):
        self.assertEqual(
            self.parser.parse('{ me { name } }'),
            Document(definitions=[
                Query(selections=[
                    Field(selections=[Field(name='name')], name='me')
                ])
            ])
        )
        self.assertEqual(
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
            Document(definitions=[
                Query(selections=[
                    Field(
                        selections=[
                            Field(name='id'),
                            Field(name='name'),
                            Field(name='profilePic'),
                            Field(alias='avatar', name='profilePic', arguments=[
                                Argument(name='width', value=30),
                                Argument(name='height', value=30)
                            ])
                        ],
                        name='user',
                        arguments=[Argument(name='id', value=4)]
                    )
                ])
            ])
        )

    def test_with_fragments(self):
        self.assertEqual(
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
                  profilePic(size: "small")
                }
            """),
            Document(definitions=[
                Query(name='withNestedFragments',
                    selections=[
                        Field(selections=[
                            Field(selections=[
                                    FragmentSpread(name='friendFields')
                                ],
                                name='friends',
                                arguments=[
                                    Argument(name='first', value=10)
                                ]),
                            Field(selections=[
                                    FragmentSpread(name='friendFields')
                                ],
                                name='mutualFriends',
                                arguments=[
                                    Argument(name='first', value=10)
                                ])
                        ],
                        name='user',
                        arguments=[Argument(name='id', value=4)])
                    ]
                ),
                FragmentDefinition(type_condition=NamedType(name='User'),
                    name='friendFields',
                    selections=[
                        Field(name='id'),
                        Field(name='name'),
                        FragmentSpread(name='standardProfilePic')
                    ]
                ),
                FragmentDefinition(type_condition=NamedType(name='User'),
                    name='standardProfilePic',
                    selections=[
                        Field(name='profilePic',
                            arguments=[Argument(name='size', value='small')]
                        )
                ])
            ])
        )

    def test_shorthand_query_with_fragments(self):
        self.assertEqual(
            self.parser.parse("""
                {
                  hero {
                    name
                    ...DroidFields
                  }
                }

                fragment DroidFields on Droid {
                  primaryFunction
                }
            """),
            Document(definitions=[
                Query(selections=[
                    Field(
                        name='hero',
                        selections=[
                            Field(name='name'),
                            FragmentSpread(name='DroidFields'),
                        ]
                    ),
                ]),
                FragmentDefinition(type_condition=NamedType(name='Droid'),
                    name='DroidFields',
                    selections=[Field(name='primaryFunction')]
                ),
            ])
        )

    def test_shorthand_vs_query(self):
        self.assertEqual(
            self.parser.parse("""
               query {
                  hero {
                    name
                  }
               }
            """),
            self.parser.parse("""
               {
                  hero {
                    name
                  }
               }
            """),
        )

    def test_variables(self):
        self.assertEqual(
            self.parser.parse("""
                query withVariable($userId: Int = 0, $userName: String) {
                  user(id: $userId, name: $userName) {
                    nick
                  }
                }
            """),
            Document(definitions=[Query(
                name='withVariable',
                variable_definitions=[VariableDefinition(
                    name='userId',
                    type=NamedType(name='Int'),
                    default_value=0
                ), VariableDefinition(
                    name='userName',
                    type=NamedType(name='String')
                )],
                selections=[Field(
                    selections=[Field(name='nick')],
                    name='user',
                    arguments=[Argument(
                        name='id',
                        value=Variable(name='userId'),
                    ), Argument(
                        name='name',
                        value=Variable(name='userName')
                    )]
                )])
            ])
        )

    def test_arguments(self):
        self.assertEqual(
            self.parser.parse("""
                {
                  episodes (number: null, isPrequel: false) {
                    id
                  }
                }
            """),
            Document(definitions=[Query(
                selections=[Field(
                    selections=[Field(name='id')],
                    name='episodes',
                    arguments=[Argument(
                        name='number',
                        value=None
                    ), Argument(
                        name='isPrequel',
                        value=False
                    )]
                )])
            ])
        )

    def test_with_subscription(self):
        self.assertEqual(
            self.parser.parse("""
                subscription onSomething($deviceId: ID!) {
                    onSomething(deviceId: $deviceId,) {
                        deviceId
                        deviceType
                        datapoints {
                            id
                        }
                    }
                }
            """),
            Document(definitions=[
                Subscription(
                    name="onSomething",
                    selections=[
                        Field(
                            name="onSomething",
                            arguments=[Argument(
                                name="deviceId",
                                value=Variable(
                                    name="deviceId"
                                )
                            )],
                            selections=[
                                Field(
                                    name="deviceId"
                                ),
                                Field(
                                    name="deviceType"
                                ),
                                Field(
                                    name="datapoints",
                                    selections=[
                                        Field(name="id")
                                    ]
                                )
                            ]
                        )
                    ],
                    variable_definitions=[
                        VariableDefinition(
                            name="deviceId",
                            type=NonNullType(
                                type=NamedType(
                                    name="ID"
                                )
                            )
                        )
                    ]
                )
            ])
        )
