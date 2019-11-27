import unittest
import legendary_eureka


class GlassdoorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.glassdoor = legendary_eureka.Glassdoor()

    def tearDown(self) -> None:
        self.glassdoor = None

    def test_get_jobs(self):
        """
        Test all get_jobs function with all possible parameters.
        """
        for i in range(4):
            sub_tests = ['all params', 'title and location', 'only title', 'wrong location']
            current_sub_test = sub_tests[i]

            with self.subTest(current_sub_test):

                if i == 0:
                    self.assertTrue(
                        self.glassdoor.get_jobs(
                            job_title='Engineer',
                            job_location='Haifa',
                            job_type='fulltime')
                    )

                elif i == 1:
                    self.assertTrue(
                        self.glassdoor.get_jobs(
                            job_title='Engineer',
                            job_location='Haifa')
                    )

                elif i == 2:
                    self.assertTrue(
                        self.glassdoor.get_jobs(
                            job_title='Engineer')
                    )

                else:
                    # Check false for city which not in Israel.
                    self.assertFalse(
                        self.glassdoor.get_jobs(
                            job_title='Engineer',
                            job_location='Miami')
                    )


if __name__ == '__main__':
    unittest.main()
