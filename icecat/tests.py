from django.test import TestCase
from django.test import SimpleTestCase
from commerce.models import Manufacturer

from icecat.models import Manufacturer, ManufacturerAlreadyMatchedException, ManufacturerExistsOnShopException
import unittest

# Create your tests here.


class IcecatImportTests(TestCase):

    def setUp(self):
        icecat_cat = Manufacturer.objects.create(
            name="Canon", icecat_id=2, logo_url="https://www.google.com")
        manufacturer = Manufacturer.objects.create(name="Canon 2")
        icecat_cat.shop_manufacturer = manufacturer
        icecat_cat.save()

    @unittest.expectedFailure
    def test_icecatmanufacturer_import(self):
        obj = Manufacturer.objects.filter(name="Canon").first()
        self.assertTrue(obj.create_shop_manufacturer(), msg='Created ok')

    @unittest.expectedFailure
    def test_icecatmanufacturer_samename_import(self):
        obj = Manufacturer.objects.filter(name="Canon").first()
        with self.assertRaises(ManufacturerExistsOnShopException, msg='Failed for manufacturer exists'):
            obj.create_shop_manufacturer()

    def test_icecatmanufacturer_alreadymatched_import(self):
        obj = Manufacturer.objects.filter(name="Canon").first()
        with self.assertRaises(ManufacturerAlreadyMatchedException, msg='Failred for manufacturere already matched'):
            obj.create_shop_manufacturer()
