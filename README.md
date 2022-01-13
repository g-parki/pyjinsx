# pyjinsx

Lightweight Python templating library for common HTML components.

## Install:
1. Clone this repository
2. Copy contents to a new folder your site-packages directory
3. Install jinja2: `pip install jinja2`

***

## Import:
``` python
    from pyjinsx import Component, Image, Div, Link, ComponentCollection
```
***

## Available components:

| Component     | Required Arguments | Optional Keyword Arguments     |
| ---        |    ----  |          --- |
| Component      | None       | id, style, classes, template_path, template_override, head_scripts, base_scripts   |
| Image   | src, alt        | id, style, classes, template_path, template_override, head_scripts, base_scripts      |
| Link   | href, contents        | id, style, classes, template_path, template_override, head_scripts, base_scripts     |
| Div   | contents        | id, style, classes, template_path, template_override, head_scripts, base_scripts      |
| ComponentCollection   | collections        | id, style, classes, template_path, template_override, head_scripts, base_scripts      |

## Public Methods:
### `Component.render()`
Returns rendered string from the template and provided arguments.
### `Component.to_file(filename: str)`
Writes rendered output to file location.

## Functions
### `template_paths(template_path: Union[str, Iterable[str]])`
Provide location for jinja2 to look for templates. The default location is a `templates` folder in your current directory.

## Examples
### Basic usage
```python
    from pyjinsx import Div, Link

    link = Link("https://github.com/g-parki/pyjinsx", "repository!") 

    print(Div(f'Here is my {link}'))

    # <div>Here is my <a href="https://github.com/g-parki/pyjinsx">repository!</a></div>
```
### Custom component
```python
    from pyjinsx import Component

    class Project(Component):

        # Name of template in templates folder
        template_path = '_project.html'

        # List all required fields
        def __init__(
            self,
            title: str,
            demo: str,
            subheading: str,
            repository: str,
            description: str,
            **kwargs
        ):
            # Pass leftover keyword arguments to Component
            super().__init__(**kwargs)
            # Provide data to template through props
            self._add_props({
                'title': title,
                'demo': demo,
                'subheading': subheading,
                'repository': repository,
                'description': description,
            })
    
    project = Project(title='', demo='', subheading='', repository='', description='').render()
```