import unittest
import api_helpers
import csv_helpers

class TestMainModuleFunctions(unittest.TestCase):
    def test_user_profile(self):
        user_data = api_helpers.get_user_profile("varunchilukuri655")
        self.assertEqual(user_data.get('followers', 0), 0)
        self.assertEqual(user_data.get('following', 0), 2)
        print("user profile - test case passed.....")

    def test_user_repository(self):
        repo_data=api_helpers.get_repository_info("varunchilukuri655","Test")
        self.assertEqual(repo_data.get('forks_count', 0), 0)
        self.assertEqual(repo_data.get('watchers_count', 0), 0)
        print("user repository - test case passed.....")

    def test_csv_file(self):
        csv_data = csv_helpers.read_from_csv("nfs-ganesha-ci-tests.csv")
        self.assertEqual(csv_data[0], 3)
        self.assertEqual(csv_data[1], 628)
        self.assertEqual(csv_data[2], 0)
        self.assertEqual(csv_data[3], 3)
        print("csv file data - test case passed.....")
        
        

if __name__ == '__main__':
    unittest.main()
