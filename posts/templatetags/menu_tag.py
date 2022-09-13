from django import template

register = template.Library()


@register.simple_tag()
def get_menu():
    menu = [
        {"name": "Posts", "url": "post_list"},
        {"name": "Users", "url": "user_list"},
        {"name": "Tags", "url": "tag_list"},
    ]
    return menu
