import unittest

from app import app, db, ma


class MyTestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		# dont provide this then the sql database is in-memory
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
		cls.app = app.test_client()
		db.init_app(app)
		# ma.init_app(app)
		with app.app_context():
			db.drop_all()
			db.create_all()

	@classmethod
	def tearDownClass(cls) -> None:
		with app.app_context():
			db.session.remove()

	def test_01_root(self):
		response = self.app.get("/", follow_redirects=True)
		self.assertEqual(response.data, b"Hello! my first flask app")
		self.assertEqual(response.status_code, 200)

	def test_02_get_zero_items(self):
		response = self.app.get("/items", follow_redirects=True)
		items = {"items": []}
		self.assertDictEqual(response.get_json(), items)

	def test_03_post_one_chair(self):
		response = self.app.post("/item/chair", json={"price": "15.67"},
								 follow_redirects=True)
		self.assertDictEqual(response.json, {'id': 1, 'name': 'chair', 'price': 15.67})

	# @unittest.SkipTest
	def test_04_post_one_table(self):
		response = self.app.post("/item/table", json={"price": "6.2"},
								 follow_redirects=True)
		self.assertDictEqual(response.json, {'id': 2, 'name': 'table', 'price': 6.2})

	def test_05_get_table(self):
		response = self.app.get("/item/table", follow_redirects=True)
		self.assertDictEqual(response.json, {'id': 2, 'name': 'table', 'price': 6.2})

	def test_06_get_all(self):
		response = self.app.get("/items", follow_redirects=True)
		items = {"items": [{'id': 1, 'name': 'chair', 'price': 15.67}, {'id': 2, 'name': 'table', 'price': 6.2}]}
		self.assertDictEqual(response.json, items)

	def test_07_put_table(self):
		response = self.app.put("/item/table", json={"price": "20.56"}, follow_redirects=True)
		self.assertDictEqual(response.json, {'id': 2, 'name': 'table', 'price': 20.56})

	def test_08_get_all(self):
		response = self.app.get("/items", follow_redirects=True)
		items = {"items": [{'id': 1, 'name': 'chair', 'price': 15.67}, {'id': 2, 'name': 'table', 'price': 20.56}]}
		self.assertDictEqual(response.json, items)


if __name__ == '__main__':
	unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1
	unittest.main()
