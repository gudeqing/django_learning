from django.test import TestCase

# Create your tests here.
# coding=utf-8
class TestFunction(unittest.TestCase):
    """
    This is test for the tool. Just run this script to do test.
    """
    def test(self):
        import random
        from mbio.workflows.single import SingleWorkflow
        from biocluster.wsheet import Sheet
        test_dir='/mnt/ilustre/users/sanger-dev/biocluster/src/mbio/tools//test_files'
        data = {
            "id": "" + str(random.randint(1, 10000)),
            "type": "tool",
            "name": ".",
            "instant": False,
            "options": dict(
           ...
            )
           }
        wsheet = Sheet(data=data)
        wf = SingleWorkflow(wsheet)
        wf.run()


if __name__ == '__main__':
    unittest.main()
