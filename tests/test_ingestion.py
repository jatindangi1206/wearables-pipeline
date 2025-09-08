import unittest
from src.ingestion import ingest_data

class TestIngestion(unittest.TestCase):
    def test_ingest_data(self):
        data = ingest_data('config.yaml')
        
        self.assertIn('blood_pressure', data)
        self.assertIn('heart_rate', data)
        self.assertIn('sleep', data)
        self.assertIn('spo2', data)
        self.assertIn('steps', data)
        self.assertIn('temperature', data)
        self.assertIn('meal', data)
        self.assertIn('lung_function', data)
        
        self.assertGreater(len(data['blood_pressure']), 0)
        self.assertGreater(len(data['heart_rate']), 0)
        self.assertGreater(len(data['sleep']), 0)
        self.assertGreater(len(data['spo2']), 0)
        self.assertGreater(len(data['steps']), 0)
        self.assertGreater(len(data['temperature']), 0)
        self.assertGreater(len(data['meal']), 0)
        self.assertGreater(len(data['lung_function']), 0)

if __name__ == '__main__':
    unittest.main()