from foodapp.models import Menu


def get_menu_by_id(id):
    return Menu.objects.get(id=id)

