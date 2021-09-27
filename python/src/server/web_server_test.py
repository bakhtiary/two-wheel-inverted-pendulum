from construct.lib import Container

from web_server import get_form

def test_get_form():
    cd = Container(pp="5", tt="0.6")
    print(cd.items())
    print(get_form(cd))


if __name__ == "__main__":
    test_get_form()

