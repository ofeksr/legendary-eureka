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

        def zero():
            return self.assertIsInstance(
                self.glassdoor.get_jobs(
                    job_title='Engineer',
                    job_location='Haifa',
                    job_type='fulltime'),
                dict
            )

        def one():
            return self.assertIsInstance(
                self.glassdoor.get_jobs(
                    job_title='Java',
                    job_location='Tel Aviv'),
                dict
            )

        def two():
            return self.assertIsInstance(
                self.glassdoor.get_jobs(
                    job_title='Python Developer'),
                dict
            )

        def three():
            return self.assertFalse(
                self.glassdoor.get_jobs(
                    job_title='Engineer',
                    job_location='Miami'
                )
            )

        def sub_tests(key):
            switcher = {
                0: zero,
                1: one,
                2: two,
                3: three,
            }
            return switcher.get(key, 'Invalid test key')

        for i in range(4):
            sub_tests_names = ['all params', 'title and location', 'only title', 'wrong location']

            with self.subTest(sub_tests_names[i]):
                func = sub_tests(i)
                func()


if __name__ == '__main__':
    unittest.main()
