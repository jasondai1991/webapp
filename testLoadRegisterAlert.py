import unittest
from loadRegister import LoadRegister

class TestLoadRegisterAlert(unittest.TestCase):

	#create a load register, and insert 11 datapoints
	def setUp(self):
		self.lg = LoadRegister(interval=10,monitortime=10*60,error_interval=2*60)
		for i in range(0,11):
			self.lg.register_load(curload=1.0)


	def test_less_than_2_minutes_generate_no_message(self):
		messages = self.lg.get_messages()
		self.assertEqual(0, len(messages))

	def test_avg_less_than_1_has_no_error(self):
		self.lg.register_load(curload = 0.9)
		messages = self.lg.get_messages()
		self.assertEqual(0, len(messages))

	def test_avg_more_than_1_has_error(self):
		self.lg.register_load(curload = 0.9)
		self.lg.register_load(curload = 1.5)
		messages = self.lg.get_messages()
		self.assertEqual(1, len(messages))
		self.assertTrue(messages[0].startswith("High load generated an alert - load"))

	def test_error_persists_and_continue(self):
		self.lg.register_load(curload = 0.9)
		self.lg.register_load(curload = 1.5)
		# even current load drops below 1, the average is still above 1 and should generate another message
		self.lg.register_load(curload = 0.9)
		messages = self.lg.get_messages()
		self.assertEqual(2, len(messages))
		self.assertTrue(messages[0].startswith("High load generated an alert - load"))
		self.assertTrue(messages[1].startswith("High load generated an alert - load"))

	#this test will test two things:
	#1. Avg drops below 1 has recover message
	#2. Old message still exists
	def test_avg_drops_below_1_has_recover_alert_and_old_message_existing(self):
		self.lg.register_load(curload = 0.9)
		self.lg.register_load(curload = 1.5)
		self.lg.register_load(curload = 0.2)
		messages = self.lg.get_messages()
		self.assertEqual(2, len(messages))
		self.assertTrue(messages[0].startswith("Load return to below 1"))
		self.assertTrue(messages[1].startswith("High load"))

if __name__ == '__main__':
    unittest.main()
