from django import template

register = template.Library()


@register.simple_tag()
def get_menu():
    menu = [{"name": "Posts", "url": "/"},
            {"name": "Users", "url": "/users"},
            {"name": "Tags", "url": "/tags"},
            {"name": "Reset DB", "url": "/create_db"}]
    return menu
