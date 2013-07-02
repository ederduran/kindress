from django.test import TestCase

from kore.models import Feed

class SimpleTest(TestCase):
  def setUp(self):
    Feed.objects.create(name="Ars")

  def Get(self):
      self.assertEqual(1 + 1, 2)
