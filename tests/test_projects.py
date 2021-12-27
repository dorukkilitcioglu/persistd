from persistd.util import projects
from tests.base_test import BaseTest, TEST_DATA_DIR


class ProjectsTest(BaseTest):
    def test_get_all_projects(self):
        # All projects, even if not initialized
        self.assertListEqual(['a', 'b'], projects.get_all_projects(TEST_DATA_DIR))

        # Only initialized projects
        self.assertListEqual(['a'], projects.get_all_projects(TEST_DATA_DIR, only_initialized=True))
