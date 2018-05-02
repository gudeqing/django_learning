# coding=utf-8
import os
import glob
from biocluster.agent import Agent
from biocluster.tool import Tool
from biocluster.core.exceptions import OptionError
import unittest
# import pandas as pd
__author__ = 'who'


class ClusterAgent(Agent):
    """
    cluster description
    """
    def __init__(self, parent):
        super(ClusterAgent, self).__init__(parent)
        options = [
            {'name': 'exp_matrix', 'type': 'infile', 'default': 'None', 'format': 'ref_rna.exp_matrix'},
            {'name': 'scm', 'type': 'string', 'default': 'Average', 'format': 'None'},
            {'name': 'scd', 'type': 'string', 'default': 'Euclidean', 'format': 'None'},
        ]
        self.add_option(options)

    def check_options(self):
        pass

    def set_resource(self):
        self._cpu = 4
        self._memory = "{}G".format('15')

    def end(self):
        result_dir = self.add_upload_dir(self.output_dir)
        result_dir.add_relpath_rules([
            [".", "", "Cluster"]
            ])
        """
        # more detail
        result_dir.add_regexp_rules([
            [r"*.xls", "xls", "xxx"],
            [r"*.list", "", "xxx"],
        ])
        """
        super(ClusterAgent, self).end()


class ClusterTool(Tool):
    """
    cluster description
    """
    def __init__(self, config):
        super(ClusterTool, self).__init__(config)
        software_dir = self.config.SOFTWARE_DIR
        self.python_path = 'program/Python/bin/python'
        self.cluster = self.config.PACKAGE_DIR + '/ref_rna/cluster.py'
        self.gcc = software_dir + '/gcc/5.1.0/bin'
        self.gcc_lib = software_dir + '/gcc/5.1.0/lib64'
        self.set_environ(PATH=self.gcc, LD_LIBRARY_PATH=self.gcc_lib)
        self.r_path = software_dir + "/program/R-3.3.1/bin:$PATH"
        self._r_home = software_dir + "/program/R-3.3.1/lib64/R/"
        self._LD_LIBRARY_PATH = software_dir + "/program/R-3.3.1/lib64/R/lib:$LD_LIBRARY_PATH"
        self.set_environ(PATH=self.r_path, R_HOME=self._r_home, LD_LIBRARY_PATH=self._LD_LIBRARY_PATH)

    def run_cluster(self):
        cmd = '{} {} '.format(self.python_path, self.cluster)
        cmd += '-{} {} '.format("exp_matrix", self.option("exp_matrix").prop['path'])
        cmd += '-{} {} '.format("scm", self.option("scm"))
        cmd += '-{} {} '.format("scd", self.option("scd"))
        cmd_name = 'cluster'
        command = self.add_command(cmd_name, cmd)
        command.run()
        self.wait()
        if command.return_code == 0:
            self.logger.info("{} Finished successfully".format(cmd_name))
        elif command.return_code is None:
            self.logger.warn("{} Failed and returned None, we will try it again.".format(cmd_name))
            command.rerun()
            self.wait()
            if command.return_code is 0:
                self.logger.info("{} Finished successfully".format(cmd_name))
            else:
                self.set_error("{} Failed. >>>{}".format(cmd_name, cmd))
        else:
            self.set_error("{} Failed. >>>{}".format(cmd_name, cmd))

    def set_output(self):
        target_files = glob.glob(self.work_dir + '/*_vs_*.xls')
        ......
        target_files += glob.glob(self.work_dir + '/result.xls')
        for each in target_files:
            name = os.path.basename(each)
            link = os.path.join(self.output_dir, name)
            if os.path.exists(link):
                os.remove(link)
            os.link(each, link)

    def run(self):
        super(ClusterTool, self).run()
        self.run_cluster()
        self.set_output()
        self.end()


class TestFunction(unittest.TestCase):
    """
    This is test for the tool. Just run this script to do test.
    """
    def test(self):
        import random
        from mbio.workflows.single import SingleWorkflow
        from biocluster.wsheet import Sheet
        data = {
            "id": "Cluster" + str(random.randint(1, 10000)),
            "type": "tool",
            "name": "ref_rna.cluster",
            "instant": False,
            "options": dict(
                exp_matrix="None",
                scm="Average",
                scd="Euclidean",
            )
           }
        wsheet = Sheet(data=data)
        wf = SingleWorkflow(wsheet)
        wf.run()


if __name__ == '__main__':
    unittest.main()/n