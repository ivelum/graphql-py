graphql-py
==========

.. image:: https://travis-ci.org/ivelum/graphql-py.svg?branch=master
        :target: https://travis-ci.org/ivelum/graphql-py

GraphQL lexer and parser written in Python, produces AST. Features:

* Complies with latest `working draft of GraphQL specification`_;
* Fast enough, built on `PLY`_;
* Tested vs. Python 2.7, 3.4 and PyPy

.. _working draft of GraphQL specification: https://facebook.github.io/graphql/
.. _PLY: http://www.dabeaz.com/ply/

Installation
------------

.. code:: shell

    $ pip install graphql-py

Usage
-----

.. code:: shell

    from graphql.parser import GraphQLParser
    
    parser = GraphQLParser()
    ast = parser.parse("""
    {
      user(id: 4) {
        id
        name
        profilePic
        avatar: profilePic(width: 30, height: 30)
      }
    }
    """)
    print(ast) 

Work in progress
----------------

Next I plan to add schema definition and provide a layer for binding real 
applications logic, so we can have a fully-functional GraphQL server. Django
support is also planned, probably as a separate package.
