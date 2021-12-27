import os
import tempfile

from persistd.util.settings import Settings, SETTINGS
from tests.base_test import BaseTest


class SettingsTest(BaseTest):
    def test_settings_update(self):
        with tempfile.TemporaryDirectory() as dirname:
            temp_file = os.path.join(dirname, 'settings.json')
            settings = Settings.load(temp_file, missing_ok=True)
            setattr(settings, 'base_path', 'dummy/path')
            self.assertEqual(settings.base_path, 'dummy/path')
            settings.save()
            settings2 = Settings.load(temp_file)
            self.assertEqual(settings.base_path, settings2.base_path)

    def test_field_names(self):
        names = SETTINGS.field_names()
        for field in names:
            self.assertTrue(isinstance(field, str))

    def test_add_open_project(self):
        with tempfile.TemporaryDirectory() as dirname:
            temp_file = os.path.join(dirname, 'settings.json')
            settings = Settings.load(temp_file, missing_ok=True)
            self.assertListEqual(settings.open_projects, [])

            settings.add_open_project('a')
            self.assertListEqual(settings.open_projects, ['a'])

            # Test if it was automatically saved
            settings2 = Settings.load(temp_file)
            self.assertListEqual(settings2.open_projects, ['a'])

            # Test if auto saving can be turned off
            settings.add_open_project('b', save=False)
            settings3 = Settings.load(temp_file)
            self.assertListEqual(settings3.open_projects, ['a'])

            # Test relaunching same project
            with self.assertRaises(ValueError):
                settings.add_open_project('a')

    def test_remove_open_project(self):
        with tempfile.TemporaryDirectory() as dirname:
            temp_file = os.path.join(dirname, 'settings.json')
            settings = Settings.load(temp_file, missing_ok=True)

            settings.add_open_project('a')
            self.assertListEqual(settings.open_projects, ['a'])
            settings.remove_open_project('a')
            # Test if it was automatically saved
            settings2 = Settings.load(temp_file)
            self.assertListEqual(settings2.open_projects, [])

            # Test if auto saving can be turned off
            settings.add_open_project('b')
            settings.remove_open_project('b', save=False)
            settings3 = Settings.load(temp_file)
            self.assertListEqual(settings3.open_projects, ['b'])

            # Test re-removing same project
            with self.assertRaises(ValueError):
                settings.remove_open_project('c')
