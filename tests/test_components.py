from ..pyjinsx import *
import pytest

def test_image():
    output = '<img id="2" src="source" alt="alt">'
    img = Image("source", "alt", id=2).render()
    assert(img == output)

def test_link():
    output = '<a class="my-class" href="url">Text</a>'
    link = Link("Text", "url", classes="my-class").render()
    assert(link == output)

def test_div():
    output = '<div style="my style">Text</div>'
    div = Div("Text", style="my style").render()
    assert(div == output)  

def test_p():
    output = '<p style="my style">Text</p>'
    p = P("Text", style="my style").render()
    assert(p == output)

def test_template_override():
    my_div = Div("world", template_override="Hello {{contents}}").render()
    assert(my_div == "Hello world")

def test_contentonly_tagless():
    class Tagless(ContentOnly):
        pass
    with pytest.raises(ValueError):
        _ = Tagless("content")

def test_convenience_syntax():
    output = '<p id="id" class="my-class" style="my styles">Text</p>'
    p = P("Text").classes("my-class").id("id").style("my styles").render()
    assert(p == output)