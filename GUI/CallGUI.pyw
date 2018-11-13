import sys
from wf_GUI_test import *
from PyQt5 import QtWidgets
from bioblend.galaxy import GalaxyInstance


class MyForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        gi = GalaxyInstance('http://localhost:8080/', email='admin@galaxy.org', password='admin')
        wf_id = [wf["id"] for wf in gi.workflows.get_workflows() if
                 wf['name'] == "WF_WithDatasets (imported from uploaded file)"][0]
        wf = gi.workflows.show_workflow(wf_id)
        wf_inputs = wf['inputs']
        str_inputs = ""
        for inp, data in wf_inputs.items():
            str_inputs += data["label"]
            str_inputs += "\n"
        self.ui.label.setText(str_inputs)
        self.ui.label.setFixedHeight(30)
        self.ui.label.setFixedWidth(300)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())

