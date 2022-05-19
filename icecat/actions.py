
import gzip
import os
import requests
from icecat.models import IcecatCategory
from shop.settings import BASE_DIR, env
import xml.etree.ElementTree as ET

categories_path_gz = f"{BASE_DIR}/external_data/CategoriesList.xml.gz"
categories_xml_path = f"{BASE_DIR}/external_data/CategoriesList.xml"


def download_icecat_categories_file():
    username = env("ICECAT_USERNAME")
    password = env("ICECAT_PASSWORD")
    link = f"https://{username}:{password}@data.icecat.biz/export/freexml.int/refs/CategoriesList.xml.gz"
    path_gz = f"{BASE_DIR}/external_data/CategoriesList.xml.gz"
    content = requests.get(link).content
    if content:
        file_gz = open(path_gz, "wb")
        file_gz.write(content)
        file_gz = gzip.open(path_gz, "rb")
        return True
    return False


def unzip_icecat_categories_file():
    file_xml = open(categories_xml_path, "wb")
    file_gz = open(categories_path_gz, "wb")
    file_xml.write(file_gz.read())
    file_xml.close()


def parse_icecat_categories_file():
    tree = ET.parse(categories_xml_path)
    root = tree.getroot()

    for category in root.findall('./Response/CategoriesList/Category'):

        if IcecatCategory.objects.filter(icecat_id=category.attrib["ID"]).count() == 0:
            new_cat = IcecatCategory()
            names = category.findall("Name")

            for name in names:
                if name.attrib["langid"] == "5":
                    new_cat.name = name.attrib["Value"]
            new_cat.icecat_id = category.attrib["ID"]
            parent_category = category.find("ParentCategory")
            if parent_category:
                try:
                    new_cat.parent_icecat_id = int(
                        parent_category.attrib["ID"])
                except:
                    pass

            if len(new_cat.name) > 1:
                new_cat.save()
    if os.path.exists((categories_path_gz)):
        os.remove(categories_path_gz)
    return True


def connect_icecat_categories():
    for category in IcecatCategory.objects.exclude(parent_icecat_id=None):
        try:
            category.parent = IcecatCategory.objects.get(
                icecat_id=category.parent_icecat_id)
            category.save()
        except:
            pass
    return True


def create_root_icecat_category():

    if IcecatCategory.objects.filter(icecat_id=1).count() == 0:
        cat = IcecatCategory()
        cat.name = "Root"
        cat.icecat_id = 1
        cat.save()
