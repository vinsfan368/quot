#!/usr/bin/env python
"""
Launcher.py -- a simple menu that provides options to launch
other, more specialized GUIs

"""
import sys

# File paths
import os 
from glob import glob 

# Main GUI utilities
import PySide6
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QApplication, QWidget, QLabel, \
    QPushButton, QVBoxLayout

# Custom GUI utilities
from .guiUtils import (
    set_dark_app,
    getOpenFilePath,
    getOpenDirectory,
    split_channels_nd2,
    SingleComboBoxDialog
)
from .imageViewer import ImageViewer 
from .detectViewer import DetectViewer 
from .spotViewer import SpotViewer 
from .attributeViewer import AttributeViewer 
from .trackViewer import TrackViewer 
from .masker import Masker 
from .maskInterpolator import MaskInterpolator

class Launcher(QWidget):
    """
    Simple GUI that presents the user with a list of options
    to launch other GUIs. Pressing on a button will prompt
    the user to select files or settings required to launch
    the corresponding GUI.

    init
    ----
        parent      :   root QWidget, if any 
        currdir     :   str, the default directory for file
                        selection dialogs

    """
    def __init__(self, currdir=None, parent=None):
        super(Launcher, self).__init__(parent)

        # Set default directory for file selection dialogs
        if currdir is None:
            currdir = os.getcwd()
        self.currdir = currdir

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface.

        """
        # Main vertical box layout
        L = QVBoxLayout(self)

        # Title
        title = QLabel(parent=self)
        title.setText("Single particle tracking utilities")
        L.addWidget(title, 0, alignment=Qt.AlignTop)

        # Buttons to launch subGUIs
        button_ids = [
            ("Simple image viewer", self.launch_image_viewer),
            ("Detection viewer", self.launch_detect_viewer),
            ("Spot viewer", self.launch_spot_viewer),
            ("Track viewer", self.launch_track_viewer),
            ("Attribute viewer", self.launch_attribute_viewer),
            ("Simple masker", self.launch_masker),
            ("Mask interpolator", self.launch_mask_interpolator),
            ("Split channels", self.split_channels)
        ]
        self.buttons = []
        for i, (label, callback) in enumerate(button_ids):
            self.buttons.append(QPushButton(label, parent=self))
            L.addWidget(self.buttons[-1], i+1, alignment=Qt.AlignTop)
            self.buttons[-1].clicked.connect(callback)

        # Show the window
        self.show()

    def launch_image_viewer(self):
        """
        Launch an instance of ImageViewer on a sample file, 
        which is a simple viewer for movies.

        """
        # Prompt the user to enter a target image file
        path = getOpenFilePath(self, "Select image file",
            "Image files (*.nd2 *.tif *.tiff)",
            initialdir=self.currdir)

        # If this is a real file, launch an ImageViewer on it
        if os.path.isfile(path):
            I = ImageViewer(path, parent=self)

    def launch_detect_viewer(self):
        """
        Launch an instance of DetectViewer on a sample file.

        """
        # Prompt the user to enter a target image file
        path = getOpenFilePath(self, "Select image file",
            "Image files (*.nd2 *.tif *.tiff)",
            initialdir=self.currdir)

        # If this is a real file path, launch a DetectViewer 
        # on it
        if os.path.isfile(path):
            self.currdir = os.path.dirname(path)
            V = DetectViewer(path, parent=self)


    def launch_spot_viewer(self):
        """
        Launch an instance of SpotViewer on a sample file.

        """
        # Prompt the user to enter a set of localizations
        path = getOpenFilePath(self, "Select locs CSV",
            "CSV files (*.csv)", initialdir=self.currdir)

        # Check that this is a real file path
        if not os.path.isfile(path):
            print("path %s does not exist" % path)
            return 
        else:
            self.currdir = os.path.dirname(path)

        # Try to find the corresponding image file
        image_file = None 
        if "_tracks.csv" in path:
            nd2_file = path.replace("_tracks.csv", ".nd2")
            tif_file = path.replace("_tracks.csv", ".tif")
            if os.path.isfile(nd2_file):
                image_file = nd2_file
            elif os.path.isfile(tif_file):
                image_file = tif_file

        # Otherwise prompt the user to enter the corresponding
        # image file
        if image_file is None:
            image_file = getOpenFilePath(self, "Select image file", 
                "Image files (*.nd2 *.tif *.tiff)", initialdir=self.currdir)
        else:
            print("Found matching image file %s" % image_file)

        # Check that this path exists
        if not os.path.isfile(image_file):
            print("path %s does not exist" % image_file)
            return 

        # Launch an instance of SpotViewer
        V = SpotViewer(image_file, path, parent=self)

    def launch_track_viewer(self):
        """
        Launch an instance of TrackViewer on a set of localizations
        corresponding to one file.

        """
        # Prompt the user to enter a set of localizations
        path = getOpenFilePath(self, "Select locs CSV",
            "CSV files (*.csv)", initialdir=self.currdir)

        # Check that this is a real file path
        if not os.path.isfile(path):
            print("path %s does not exist" % path)
            return 
        else:
            self.currdir = os.path.dirname(path)

        # Try to find the corresponding image file
        image_file = None 
        if "_tracks.csv" in path:
            nd2_file = path.replace("_tracks.csv", ".nd2")
            tif_file = path.replace("_tracks.csv", ".tif")
            if os.path.isfile(nd2_file):
                image_file = nd2_file
            elif os.path.isfile(tif_file):
                image_file = tif_file

        # Otherwise prompt the user to enter the corresponding
        # image file
        if image_file is None:
            image_file = getOpenFilePath(self, "Select image file", 
                "Image files (*.nd2 *.tif *.tiff)", initialdir=self.currdir)
        else:
            print("Found matching image file %s" % image_file)

        # Check that this path exists
        if not os.path.isfile(image_file):
            print("path %s does not exist" % image_file)
            return 

        # Launch an instance of TrackViewer
        V = TrackViewer(image_file, path, parent=self)

    def launch_attribute_viewer(self):
        """
        Launch an instance of AttributeViewer on a sample file.

        """
        # Prompt the user to enter a set of localizations
        path = getOpenFilePath(self, "Select locs CSV",
            "CSV files (*.csv)", initialdir=self.currdir)

        # Check that this is a real file path
        if not os.path.isfile(path):
            print("path %s does not exist" % path)
            return 
        else:
            self.currdir = os.path.dirname(path)

        # Launch an instance of AttributeViewer
        V = AttributeViewer(path, max_spots=30000, parent=self)

    def launch_masker(self):
        """
        Launch an instance of Masker on a single file.

        """
        # Prompt the user to enter a file
        path = getOpenFilePath(self, "Select image file to use for masking",
            "Image files (*.tif *.tiff *.nd2)", initialdir=self.currdir)

        # Check that this is a real file path
        if not os.path.isfile(path):
            print("path %s does not exist" % path)
            return 
        else:
            self.currdir = os.path.dirname(path)

        # Launch an instance of Masker
        V = Masker(path, parent=self)

    def launch_mask_interpolator(self):
        """
        Launch an instance of MaskInterpolator.

        """
        V = MaskInterpolator(parent=self)

    def split_channels(self):
        """
        Split ND2 files into TIF files, one for each channel.

        """
        # Single ND2 file or directory of ND2 files?
        ex = SingleComboBoxDialog("Single ND2 file or directory?", 
            options=["Single ND2 file", "Directory with ND2 files"],
            title="Select input type", parent=self)
        ex.exec_()

        # Dialog accepted
        if ex.result() == 1:
            path = ex.return_val
        else:
            return 

        if ex.return_val == "Single ND2 file":

            # Prompt the user to enter a file
            path = getOpenFilePath(self, "Select image file to split",
                "ND2 files (*.nd2)", initialdir=self.currdir)

            # Split this file
            split_channels_nd2(path, out_dir=None)

            # Give an indication of completion
            print("Successfully split channels for file {}".format(path))

        elif ex.return_val == "Directory with ND2 files":

            # Prompt the user to enter a directory
            dirname = getOpenDirectory(self, "Select directory with ND2 files", 
                initialdir=self.currdir)

            # Get all ND2 files in this directory
            nd2_paths = glob(os.path.join(dirname, "*.nd2"))

            # Split all ND2 files
            for nd2_path in nd2_paths:
                split_channels_nd2(nd2_path, out_dir=None)
                print("Successfully split channels for file {}".format(nd2_path))

def init_launcher():
    """
    Initialize a standalone instance of Launcher.

    """
    app = QApplication()
    set_dark_app(app)
    ex = Launcher()
    sys.exit(app.exec_())

if __name__ == '__main__':
    init_launcher()
