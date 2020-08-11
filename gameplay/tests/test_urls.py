from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .. import views as gameplay_views


class TestUrls(SimpleTestCase):

  def test_gameplay_home_resolves(self):
    url = reverse('gameplay_home')
    self.assertEqual(resolve(url).func, gameplay_views.home_page)

  def test_gameplay_leaderboard_resolves(self):
    url = reverse('gameplay_leaderboard')
    self.assertEqual(resolve(url).func, gameplay_views.leaderboard_page)

  def test_gameplay_matches_resolves(self):
    url = reverse('gameplay_matches')
    self.assertEqual(resolve(url).func, gameplay_views.matches_page)

  def test_gameplay_create_entry_resolves(self):
    url = reverse('gameplay_create_entry')
    self.assertEqual(resolve(url).func, gameplay_views.create_entry_page)

  def test_gameplay_entry_resolves(self):
    url = reverse('gameplay_entry', args=['1'])
    self.assertEqual(resolve(url).func, gameplay_views.entry_page)

  def test_gameplay_user_entries_resolves(self):
    url = reverse('gameplay_user_entries')
    self.assertEqual(resolve(url).func, gameplay_views.user_entries_page)

  def test_gameplay_error_resolves(self):
    url = reverse('gameplay_error')
    self.assertEqual(resolve(url).func, gameplay_views.error_page)
