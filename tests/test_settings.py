import os
import tempfile

from persistd.util.settings import LOCAL_SETTINGS_PATH, Settings, SETTINGS
from tests.base_test import BaseTest


class SettingsTest(BaseTest):
    def test_settings_update(self):
        with tempfile.TemporaryDirectory() as dirname:
            temp_file = os.path.join(dirname, 'settings.json')
            settings = Settings.load(temp_file, missing_ok=True)
            self.assertEqual(settings.file_path, LOCAL_SETTINGS_PATH)
            setattr(settings, 'file_path', temp_file)
            self.assertEqual(settings.file_path, temp_file)
            settings.save()
            settings2 = Settings.load(temp_file)
            self.assertEqual(settings.file_path, settings2.file_path)

    def test_field_names(self):
        names = SETTINGS.field_names()
        for field in names:
            self.assertTrue(isinstance(field, str))
