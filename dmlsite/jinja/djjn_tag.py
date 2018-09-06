from jinja2.ext import Extension
from jinja2.nodes import Node
from jinja2.parser import Parser
from jinja2 import lexer, nodes


class Django(Extension):
    tags = set(['django'])

    def _django(self):
        return ('<p>fvfhlnhlkvf</p>')

    def parse(self, parser: Parser) -> Node:
        lineno = next(parser.stream).lineno
        call = self.call_method('_django', lineno=lineno)
        return nodes.Output([call], lineno=lineno)
        try:
            token = parser.stream.expect(lexer.TOKEN_STRING)

        except Exception as e:
            print(e)


