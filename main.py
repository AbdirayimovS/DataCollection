'''
Scene to display a view and record webcamera and tobii tracker results.
'''
import sys
import argparse
import os

from PyQt5 import QtWidgets

from src.main_window import MainWindow
from src.secondary_window import SecondaryWindow




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Path to the file")

    args = parser.parse_args()

    os.path.dirname(args.filename)
    os.makedirs(args.filename)

    app = QtWidgets.QApplication(sys.argv)
    primary_screen = app.primaryScreen()
    screens = app.screens()
    if len(screens) < 2:
        raise RuntimeError("Program can not see second monitor! Please connect second monitor.")
    screens.remove(primary_screen)
    secondary_screen=screens[0]
    patient_window = SecondaryWindow(secondary_screen)
    experiment_dashboard = MainWindow(patient_window, args.filename)
    experiment_dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Bismillahir-Rohmanir-Rohiim!")
    main()
