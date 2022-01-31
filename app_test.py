from app import app
import unittest


class FlaskTest(unittest.TestCase):

    # Check for response 200
    def test_inde(self):
        tester = app.test_client(self)  # tester object
        response = tester.get("/sensors")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if the content return is application JSON
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/sensors")
        self.assertEqual(response.content_type, "application/json")

    # check the Data returned
    def test_id_data(self):
        tester = app.test_client(self)
        response = tester.get("/sensors/1")
        self.assertTrue(b'id' in response.data)

    # check the Data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/sensors/1")
        self.assertTrue(b'temp' in response.data)

    # check the Data returned
    def test_average_data(self):
        tester = app.test_client(self)
        response = tester.get("sensors/1/ave/7")
        self.assertTrue(b'average temp' in response.data)


if __name__ == '__main__':
    unittest.main()
