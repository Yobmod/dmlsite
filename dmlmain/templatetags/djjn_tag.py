from django import template as django_template
from jinja2 import nodes, contextfunction, ext, parser, runtime as jn_runtime, contextfilter
from django_jinja import library as djjn_library
# from coffin.template import Library as cf_library

from typing import Optional as Opt


# The actual Django templatag for Jinja
class Django(ext.Extension):
    tags = set(['django'])

    def preprocess(self, source: str, name: str, filename: Opt[str]=None) -> str:
        source = source.replace('{% django %}', '{% django %}{% raw %}')
        source = source.replace('{% enddjango %}', '{% endraw %}{% enddjango %}')
        return source

    @contextfunction
    def _django(self, context: jn_runtime.Context, html: str) -> str:
        return django(context, html)

    def parse(self, parser: parser.Parser) -> nodes.Output:
        lineno = parser.stream.next().lineno

        while not parser.stream.next().test('block_end'):
            pass

        body = nodes.Const(parser.stream.next().value)

        while not parser.stream.current.test('block_end'):
            parser.stream.next()

        return nodes.Output([
            self.call_method('_django', args=[body], kwargs=[]),
        ]).set_lineno(lineno=lineno)


# Alternatively, we can also call `django()` as a function.
# Our templatetag silently converts the Django tag to this function call


@contextfunction
@djjn_library.global_function
def django(context: django_template.Context, html: str) -> str:
    context = django_template.RequestContext(context['request'], context)
    return django_template.Template(html).render(context)
