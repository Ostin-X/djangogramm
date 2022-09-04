from django import template

register = template.Library()


@register.simple_tag()
def get_menu():
    menu = [
        {"name": "Posts", "url": "post_list"},
        {"name": "Create Post", "url": "post_create"},
        {"name": "Users", "url": "users"},
        {"name": "Tags", "url": "tag_list"},
        {"name": "Reset DB", "url": "create_db"},
        {"name": "Admin", "url": "admin:index"},
    ]
    return menu
