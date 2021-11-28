import json
import os

from django.core.management.base import BaseCommand
from roles.models import Menu


class Command(BaseCommand):
    help = "Menus Setup"

    def get_file_path(self, file_name):
        """returns absolute path of file

        Args:
            file_name (str): name of file

        Returns:
            str: absolute file_path
        """
        file_path = os.path.dirname(__file__)
        file_path += f"/data/{file_name}"

        return file_path

    def open_file(self, file_path):
        """open json file and return dict"""
        with open(file_path, "r") as fp:
            data: dict = json.loads(fp.read())
        return data

    def get_or_create_menu(self, menu, parent=None):
        print(f"Creating menu: {menu['name']}")
        parent, _ = Menu.objects.get_or_create(
            name=menu["name"],
            code=menu["code"],
            url=menu["url"],
            ic_class=menu["ic_class"] if menu.get("ic_class", None) else None,
            defaults={"parent": parent},
        )
        return parent

    def create_child_menus(self, menu, parent):
        child_menus = menu["children"]
        while len(child_menus):
            for sub_menu in child_menus:
                sub_menu_parent = self.get_or_create_menu(sub_menu, parent)
                child_menus = sub_menu["children"]
                self.create_child_menus(sub_menu, sub_menu_parent)

    def handle(self, *args, **options):

        menus = self.open_file(self.get_file_path("menus.json"))

        for menu in menus:
            parent = self.get_or_create_menu(menu)
            if parent and menu["children"]:
                self.create_child_menus(menu, parent)

        print("All menus imported successfully.")
