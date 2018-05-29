# -*- coding: utf-8 -*-
from biocluster.workflow import Workflow


class ExpVennWorkflow(Workflow):
    """
    ExpVenn description
    """
    def __init__(self, wsheet_object):
        self._sheet = wsheet_object
        super(ExpVennWorkflow, self).__init__(wsheet_object)
        options = list()
        for each in self._sheet.options():
            options.append(dict(name=each, type="string"))
        self.add_option(options)
        self.set_options(self._sheet.options())
        self.exp_venn = self.add_tool("ref_rna.exp_venn")
        self.dump_tool = self.api.api("ref_rna.exp_venn")

    def run(self):
        # self.start_listener(); self.fire("start") # if you have no tools, you should use this line
        self.exp_venn.on("end", self.set_db)
        self.run_exp_venn()
        super(ExpVennWorkflow, self).run()

    def run_exp_venn(self):
        options = dict(
            exp_matrix=self.option('exp_matrix'),
            threshold=self.option('threshold'),
            group=self.option('group'),
        )
        self.exp_venn.set_options(options)
        self.exp_venn.run()

    def set_db(self):
        """
        dump data to db
        """
        workflow_output = self.get_workflow_output_dir()
        # add result info
        self.dump_tool.add_exp_venn_detail(self.exp_venn.output_dir, self.option("main_id"))
        self.dump_tool.update_db_record('sg_exp_venn', self.option('main_id'), output_dir=workflow_output, status="end")
        self.end()

    def end(self):
        result_dir = self.add_upload_dir(self.exp_venn.output_dir)
        result_dir.add_relpath_rules([
            [".", "", "ExpVenn"],
        ])
        super(ExpVennWorkflow, self).end()

    def get_workflow_output_dir(self):
        workflow_output = self._sheet.output
        if workflow_output.startswith('tsanger:'):
            workflow_output = workflow_output.replace('tsanger:','/mnt/ilustre/tsanger-data/')
        else:
            workflow_output = workflow_output.replace('sanger:','/mnt/ilustre/data/')
        return workflow_output