
from django import VERSION
from django import template
from django.template.loader import get_template
from django.template.base import FilterExpression, Parser, TokenType  # , Token

import jinja2
# from jinja2 import nodes.Node  # , runtime.Context, parser.Parser
from django_jinja import library

from sitetree.sitetreeapp import get_sitetree
# from ..sitetreeapp import get_sitetree

from typing import List, Union, Optional as Opt

register = template.Library()
_CONTEXT_FLATTEN = (VERSION >= (1, 11))


class sitetree_treeNode(template.Node):
    """Renders tree items from specified site tree."""

    def __init__(self, tree_alias: str, use_template: Opt[str]) -> None:
        self.use_template = use_template
        self.tree_alias = tree_alias

    def render(self, context: template.Context) -> str:
        tree_items = get_sitetree().tree(self.tree_alias, context)
        return render(context, tree_items, self.use_template or 'sitetree/tree.html')


# @register.tag
@library.global_function
def sitetree_tree(parser: Parser, token: TokenType.TEXT) -> sitetree_treeNode:
    """Parses sitetree tag parameters.
    Two notation types are possible:
        1. Two arguments:
           {% sitetree_tree from "mytree" %}
           Used to render tree for "mytree" site tree.
        2. Four arguments:
           {% sitetree_tree from "mytree" template "sitetree/mytree.html" %}
           Used to render tree for "mytree" site tree using specific
           template "sitetree/mytree.html"
    """
    tokens = token.split_contents()
    use_template = detect_clause(parser, 'template', tokens)
    tokens_num = len(tokens)

    if tokens_num in (3, 5):
        tree_alias = parser.compile_filter(tokens[2])
        return sitetree_treeNode(tree_alias, use_template)
    else:
        raise jinja2.exceptions.TemplateSyntaxError(lineno=0,
                                                    name='sitetreeError',
                                                    filename='meeehhh',
                                                    message=f"""{tokens[0]} tag requires two arguments. 
                                                            E.g. {{%% sitetree_tree from "mytree" %%}}.""")


def detect_clause(parser: Parser, clause_name: str, tokens: TokenType.TEXT) -> Opt[FilterExpression]:
    """Helper function detects a certain clause in tag tokens list. Returns its value."""

    clause_value: Opt[FilterExpression]
    if clause_name in tokens:
        t_index = tokens.index(clause_name)
        clause_value = parser.compile_filter(tokens[t_index + 1])
        del tokens[t_index:t_index + 2]
    else:
        clause_value = None
    return clause_value


def render(context: template.Context, tree_items: Union[str, List[str]], use_template: Opt[str]) -> str:
    """Render helper is used by template node functions
    to render given template with given tree items in context.
    """
    context.push()
    context['sitetree_items'] = tree_items

    if isinstance(use_template, FilterExpression):
        use_template = use_template.resolve(context)
    elif use_template is None:
        use_template = ""
    content: str = get_template(use_template).render(context.flatten() if _CONTEXT_FLATTEN else context)
    context.pop()

    return content
