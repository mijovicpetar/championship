"""Test moudle."""

import os
import unittest
import random
from json import loads, dumps
import requests


class TestApiMethods(unittest.TestCase):
    """Test api methods."""

    # Development server
    url = 'http://127.0.0.1:5000/api'
    # Production server
    # url = 'http://3.14.1.45/api'

    def publish(self):
        """Publish method."""
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(curr_dir, 'files')
        input_json_path = os.path.join(files_dir, 'input.json')
        with open(input_json_path, 'r') as json_file:
            data = json_file.read()

        res = requests.post(self.url + '/fixture/result/publish', json=data)
        res = loads(res.text)

        return res

    def test_publish(self):
        """Test publish endpoint method."""
        res = self.publish()
        if not res:
            self.fail('Publish failed.')

    def test_get_tabels(self):
        """Test get tabels endpoint method."""
        self.publish()
        res = requests.get(self.url + '/table/all')
        res = loads(res.text)
        if res == 'Error occured.':
            self.fail('Get tabels failed.')

    def filter(self, filters_dict):
        """Filter method."""
        res = requests.post(
            self.url + '/fixture/result/filter', json=filters_dict)
        res = loads(res.text)

        return res

    def test_filter_results(self):
        """Test filter results."""
        self.publish()

        filters_dict = {
            'group': 'A',
            'team': 'PSG',
            'date_from': '2017-09-13T20:45:00',
            'date_to': '2017-09-20T20:45:00'
        }
        filters_dict = dumps(filters_dict)

        res = self.filter(filters_dict)
        if res == 'Error occured.':
            self.fail('Filtering failed.')

    @classmethod
    def generate_new_score(cls, old_score):
        """Generate new score, different from old score."""
        new_home_score = random.randint(0, 5)
        new_away_score = random.randint(0, 5)
        new_score = str(new_home_score) + ':' + str(new_away_score)

        while new_score == old_score:
            new_home_score = random.randint(0, 5)
            new_away_score = random.randint(0, 5)
            new_score = str(new_home_score) + ':' + str(new_away_score)

        return new_score

    def test_update_result(self):
        """Update result test."""
        self.publish()
        # This will return all, no filter will be applied.
        filters_dict = {}
        filters_dict = dumps(filters_dict)

        res = self.filter(filters_dict)

        # Update first returned existing score with random new score.
        target_id = res[0]['id']
        new_score = TestApiMethods.generate_new_score(res[0]['score'])

        data = {
            'id': target_id,
            'score': new_score
        }
        data = dumps(data)

        res = requests.put(self.url + '/result/update', json=data)
        res = loads(res.text)
        if res == 'Error occured.':
            self.fail('Update result failed.')

        res = self.filter(filters_dict)
        updated = False
        for result in res:
            if result['id'] == target_id:
                if result['score'] == new_score:
                    updated = True

        if not updated:
            self.fail('Update result failed.')


if __name__ == "__main__":
    unittest.main()
