from jinja2 import Environment, FileSystemLoader, Template
import os
from typing import Union, Iterable

def template_paths(template_path: Union[str, Iterable[str]]) -> None:
    """Provide path to folder containing templates."""

    Component.env = Environment(
        loader= FileSystemLoader(template_path),
        trim_blocks= True,
        lstrip_blocks= True,
    )

class Component():
    """
    Base class for renderable components.

    The default location for templates is a `templates` folder of current directory.
    
    A template name must be provided either by an inheriting class or by an instance at runtime. The template
    can be either a filename in the environment (using `template_path`)
    or a literal string template (using `template_override`).

    Each child class passes arguments to the template through its `props`. This is done
    through the `_add_props()` method.
    
    """

    env = Environment(
        loader= FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
        trim_blocks= True,
        lstrip_blocks= True,
    )
    template_path: str
    _ID_CLASS_STYLES_TEMPLATE = '{% if id %} id="{{id}}"{% endif %}'\
                                '{% if classes %} class="{{classes}}"'\
                                '{% endif %}{% if style %} style="{{style}}"{% endif %}'

    def __init__(
        self,
        id= None,
        style= None,
        classes= None,
        template_path: str = '',
        template_override: str = '',
        head_scripts: Iterable[str] = [],
        base_scripts: Iterable[str] = [],
    ):

        self.template = self._get_template(template_path, template_override)
        self.head_scripts = head_scripts
        self.base_scripts = base_scripts
        self.props = {
            'id': id,
            'style': style,
            'classes': classes,
        }
    
    def render(self):
        return self.template.render(**self.props)

    def to_file(self, filename):
        with open(filename, "w") as f:
            f.writelines(self.render())

    def _add_props(self, props: dict[str, any]):
        self.props = {
            **self.props,
            **props,
        }
    
    def _get_template(self, _path, _override):
        if _override:
            return Template(_override)
        else:
            return self.env.get_template(_path or self.template_path)


    def __str__(self):
        return self.render()

class Image(Component):

    template_override = '<img' + Component._ID_CLASS_STYLES_TEMPLATE + ' src="{{src}}" alt="{{alt}}">'

    def __init__(self, src: str, alt: str, **kwargs):
        super().__init__(template_override = self.template_override, **kwargs)
        self._add_props({
            'src': src,
            'alt': alt,
        })

class Link(Component):
    
    template_override = '<a' + Component._ID_CLASS_STYLES_TEMPLATE + ' href="{{href}}">{{contents}}</a>'

    def __init__(self, href: str, contents: str, **kwargs):
        super().__init__(template_override= self.template_override, **kwargs)
        self._add_props({
            'href': href,
            'contents': contents,
        })

class Div(Component):
    
    template_override = '<div' + Component._ID_CLASS_STYLES_TEMPLATE + '>{{contents}}</div>'

    def __init__(self, contents: str, **kwargs):
        super().__init__(template_override= self.template_override, **kwargs)
        self._add_props({
            'contents': contents,
        })

class ComponentCollection(Component):
    """
    Base class for a component with one or more collections of other components. This is used
    to pass dependency scripts from the subcomponents to the larger collection.

    Each collection is passed to `props` as a rendered list.

    A template must be provided either by an inheriting class or by an instance at runtime.

    """
    
    template_path = ''

    def __init__(self, collections: dict[str, Iterable[Component]], **kwargs):
        super().__init__(**kwargs)
        self._process_collections(collections)

    def _collect_scripts(self, collection: Iterable[Component]):
        for component in collection:
            self.head_scripts = list(set([*component.head_scripts, *self.head_scripts]))
            self.base_scripts = list(set([*component.base_scripts, *self.base_scripts]))

    def _process_collections(self, collections: dict[str, Iterable[Component]]):
        for key, collection in collections.items():
            self._add_props({
                key: [str(item) for item in collection]
            })
            self._collect_scripts(collection)
    