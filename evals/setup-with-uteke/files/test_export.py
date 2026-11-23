import csv
import os
import tempfile
import unittest

from export import SAMPLE, export_orders


class ExportTest(unittest.TestCase):
    def test_writes_header_and_rows(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.csv")
            export_orders(SAMPLE, path, job_id="j1")
            with open(path) as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[0], ["order_id", "customer", "total"])
            self.assertEqual(len(rows), 4)


if __name__ == "__main__":
    unittest.main()
