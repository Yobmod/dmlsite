from jinja2 import lexer, nodes
from jinja2.ext import Extension
from jinja2 import Environment
# from jinja2.runtime import Context
from jinja2.nodes import Node
from jinja2.parser import Parser

from django.utils import timezone
from django.template.defaultfilters import date
from django.conf import settings
from datetime import datetime

# from typing import Optional as Opt  # , List, Dict
# from typing import List, cast


class DjangoNow(Extension):
    tags = set(['now'])

    def __init__(self, environment: Environment) -> None:
        super().__init__(self)
        self.allowed_formats = ['s: i: h', 
                                'd m Y',
                                'DATE_FORMAT', 
                                'DATETIME_FORMAT', 
                                'SHORT_DATE_FORMAT', 
                                'SHORT_DATETIME_FORMAT',
                                ]

    def _now(self, date_format: nodes.Const = None) -> str:
        settings.USE_L10N = True

        if date_format not in self.allowed_formats:
            print('unknown format')
        #    raise ValueError('Dateformat not recognised. Using default')
        tzinfo = timezone.get_current_timezone() if settings.USE_TZ else None
        formatted = date(datetime.now(tz=tzinfo), date_format)
        # print(f"Timexzone={tzinfo}, Date format ={date_format}, Output={formatted}")
        return(formatted)

    def parse(self, parser: Parser) -> Node:
        lineno = next(parser.stream).lineno
        try:
            token = parser.stream.expect(lexer.TOKEN_STRING)
            date_format = nodes.Const(token.value)
        except Exception as e:
            print(e)
            date_format = nodes.Const(None)
        call = self.call_method('_now', args=[date_format]).set_lineno(lineno)
        token = parser.stream.current
        # print(token)
        if token.test('name:as'):
            # print("as token found")
            next(parser.stream)
            as_var = parser.stream.expect(lexer.TOKEN_NAME)
            as_var = nodes.Name(as_var.value, 'store', lineno=as_var.lineno)
            # print(as_var)
            return nodes.Assign(as_var, call, lineno=lineno)
        else:
            return nodes.Output([call], lineno=lineno)
