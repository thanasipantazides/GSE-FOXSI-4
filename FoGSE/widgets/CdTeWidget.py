"""
A widget to show off CdTe data.
"""
import os

import numpy as np
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QBoxLayout

from FoGSE.read_raw_to_refined.readRawToRefinedCdTe import CdTeReader
from FoGSE.windows.CdTeWindow import CdTeWindow
from FoGSE.widgets.QValueWidget import QValueRangeWidget, QValueWidget, QValueTimeWidget, QValueCheckWidget
from FoGSE.widgets.layout_tools.stretch import unifrom_layout_stretch
from FoGSE.widgets.layout_tools.spacing import set_all_spacings


class CdTeWidget(QWidget):
    """
    An individual window to display CdTe data read from a file.

    Parameters
    ----------
    data_file : `str` 
        The file to be passed to `FoGSE.read_raw_to_refined.readRawToRefinedCdTe.CdTeReader()`.
        Default: None

    plotting_product : `str`
        String to determine whether an "image" and or "spectrogram" should be shown.
        Default: "image"
    """
    def __init__(self, data_file=None, name="CdTe", image_angle=0, parent=None):

        QWidget.__init__(self, parent)
        reader = CdTeReader(datafile=data_file)

        self.setWindowTitle(f"{name}")
        self.setStyleSheet("border-width: 2px; border-style: outset; border-radius: 10px; border-color: white; background-color: white;")
        self.detw, self.deth = 50, 50
        # self.setGeometry(100,100,self.detw, self.deth)
        self.setMinimumSize(self.detw, self.deth) # stops the panel from stretching and squeezing when changing times
        self.aspect_ratio = self.detw/self.deth

        # define main layouts for the status window, LED, buttons, times, and plot
        image_layout = QtWidgets.QGridLayout()
        ped_layout = QtWidgets.QGridLayout()
        value_layout = QtWidgets.QVBoxLayout()
        # image_layout.setColumnStretch(0,1)
        # image_layout.setRowStretch(0,1)

        self.panels = dict() # for all the background panels
        
        ## for CdTe image
        # widget for displaying the automated recommendation
        self._image_layout = self.layout_bkg(main_layout=image_layout, 
                                             panel_name="image_panel", 
                                             style_sheet_string=self._layout_style("white", "white"), grid=True)
        self.image = CdTeWindow(reader=reader, plotting_product="image", name=name, integrate=True, image_angle=image_angle)#, integrate=True
        # self.image.setMinimumSize(QtCore.QSize(400,400)) # was 250,250
        # self.image.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.image.setStyleSheet("border-width: 0px;")
        self._image_layout.addWidget(self.image)
        
        # image_layout.addWidget(self.image)
        # self._image_layout.setColumnStretch(0, 1)
        # self._image_layout.setRowStretch(0, 1)

        ## for CdTe pedestal
        # widget for displaying the automated recommendation
        self._ped_layout = self.layout_bkg(main_layout=ped_layout, 
                                             panel_name="ped_panel", 
                                             style_sheet_string=self._layout_style("white", "white"), grid=True)
        self.ped = CdTeWindow(reader=reader, plotting_product="spectrogram", name="", integrate=True, image_angle=image_angle)
        # self.ped.setMinimumSize(QtCore.QSize(400,200)) # was 250,250
        # self.ped.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.ped.setStyleSheet("border-width: 0px;")
        self._ped_layout.addWidget(self.ped) 
        # self._ped_layout.setColumnStretch(0, 1)
        # self._ped_layout.setRowStretch(0, 1)

        # status values
        self._value_layout = self.layout_bkg(main_layout=value_layout, 
                                             panel_name="value_panel", 
                                             style_sheet_string=self._layout_style("white", "white"))
        # self.software_stat = QValueRangeWidget(name="SW Status", value="N/A", condition={"low":0,"high":np.inf})
        # self.de_mode = QValueRangeWidget(name="DE mode", value="N/A", condition={"low":0,"high":np.inf})
        # self.cts = QValueRangeWidget(name="Ct (ct)", value="N/A", condition={"low":0,"high":np.inf})
        # self.ctr = QValueRangeWidget(name="Ct/s", value=14, condition={"low":2,"high":15})
        
        # self.frames = QValueRangeWidget(name="# frames (t,t-1)", value=8, condition={"low":2,"high":15})
        # self.frames_t = QValueRangeWidget(name="# frames (t,t-1)", value=8, condition={"low":2,"high":15})
        # self.ping = QValueRangeWidget(name="ping", value=60, condition={"low":2,"high":15})
        # self.asic_vth = QValueRangeWidget(name="ASIC (vth,dth)", value="N/A", condition={"low":2,"high":15})
        # self.asic_dth = QValueRangeWidget(name="ASIC (vth,dth)", value="N/A", condition={"low":2,"high":15})
        # self.asic_load = QValueRangeWidget(name="ASIC load", value=2, condition={"low":2,"high":15})

        # need to groupd some of these for the layout
        # self.asic_vth = QValueRangeWidget(name="ASIC VTH", value=0, condition={"low":0,"high":127}, border_colour=asic_layout_colour)
        # self.asic_dth = QValueRangeWidget(name="DTH", value=0, condition={"low":0,"high":127}, border_colour=asic_layout_colour)
        # self.asic_load = QValueRangeWidget(name="ASIC load", value=2, condition={"low":2,"high":15}, border_colour=asic_layout_colour)
        # de
        de_layout = QtWidgets.QGridLayout()
        de_layout_colour = "rgb(53, 108, 117)"
        self.software_stat = QValueTimeWidget(name="SW Status", 
                                              value="N/A", 
                                              time=2000, 
                                              condition=[int, float, np.int64], 
                                              border_colour=de_layout_colour,
                                              tool_tip_values={"ASIC VTH":QValueWidget(name="ASIC VTH", value="N/A"), 
                                                               "ASIC DTH":QValueWidget(name="ASIC DTH", value="N/A"), 
                                                               "ASIC Load":QValueWidget(name="ASIC Load", value="N/A")},
                                              name_plus="<sup>*</sup>")
        self.de_mode = QValueRangeWidget(name="DE mode", value="N/A", condition={"low":0,"high":np.inf}, border_colour=de_layout_colour)
        self.ping = QValueCheckWidget(name="Ping", value="N/A", condition={"acceptable":[("", "white")]}, border_colour=de_layout_colour)
        self.hv = QValueRangeWidget(name="HV", value="N/A", condition={"low":0,"high":200}, border_colour=de_layout_colour)
        de_layout.addWidget(self.software_stat, 0, 0, 1, 2) 
        de_layout.addWidget(self.de_mode, 1, 0, 1, 2) 
        de_layout.addWidget(self.ping, 2, 0, 1, 2) 
        de_layout.addWidget(self.hv, 3, 0, 1, 2) 
        # counts
        cts_layout = QtWidgets.QGridLayout()
        cts_layout_colour = "rgb(141, 141, 134)"
        self.cts = QValueRangeWidget(name="<span>&#931;</span> Ct", 
                                     value="N/A", 
                                     condition={"low":0,"high":np.inf}, 
                                     border_colour=cts_layout_colour,
                                     tool_tip_values={"Ct Now":"N/A", "Ct Mean":"N/A", "Ct Median":"N/A", "Ct Max.":"N/A", "Ct Min.":"N/A"},
                                     name_plus="<sup>*</sup>")
        self.ctr = QValueRangeWidget(name="<span>&#931;</span> Ct/s", 
                                     value="N/A", 
                                     condition={"low":0,"high":np.inf}, 
                                     border_colour=cts_layout_colour,
                                     tool_tip_values={"Ct Now":"N/A", "Ct Mean":"N/A", "Ct Median":"N/A", "Ct Max.":"N/A", "Ct Min.":"N/A"},
                                     name_plus="<sup>*</sup>")
        cts_layout.addWidget(self.cts, 0, 0, 1, 2) 
        cts_layout.addWidget(self.ctr, 1, 0, 1, 2) 
        # strips
        strips_layout = QtWidgets.QGridLayout()
        strips_layout_colour = "rgb(213, 105, 48)"
        self.strips = QValueWidget(name="# of det. strips", value="", separator="", border_colour=strips_layout_colour)
        self.strips_al = QValueRangeWidget(name="Pt", value=0, condition={"low":0,"high":127}, border_colour=strips_layout_colour)
        self.strips_pt = QValueRangeWidget(name="Al", value=0, condition={"low":0,"high":127}, border_colour=strips_layout_colour)
        strips_layout.addWidget(self.strips, 0, 0, 1, 2) 
        strips_layout.addWidget(self.strips_pt, 1, 0, 1, 1) 
        strips_layout.addWidget(self.strips_al, 1, 1, 1, 1) 
        # frames
        frames_layout = QtWidgets.QGridLayout()
        frames_layout_colour = "rgb(66, 120, 139)"
        self.frames = QValueWidget(name="# of rest evt. frame", value="", separator="", border_colour=frames_layout_colour)
        self.frames_t = QValueRangeWidget(name="t", value=0, condition={"low":0,"high":127}, border_colour=frames_layout_colour)
        self.frames_tm1 = QValueRangeWidget(name="t-1", value=0, condition={"low":0,"high":127}, border_colour=frames_layout_colour)
        frames_layout.addWidget(self.frames, 0, 0, 1, 2) 
        frames_layout.addWidget(self.frames_t, 1, 0, 1, 1) 
        frames_layout.addWidget(self.frames_tm1, 1, 1, 1, 1)
        # # asics
        # asic_layout = QtWidgets.QGridLayout()
        # asic_layout_colour = "rgb(234, 141, 54)"
        # self.asic = QValueWidget(name="ASIC", value="", separator="", border_colour=asic_layout_colour)
        # self.asic_vth = QValueRangeWidget(name="VTH", value=0, condition={"low":0,"high":127}, border_colour=asic_layout_colour)
        # self.asic_dth = QValueRangeWidget(name="DTH", value=0, condition={"low":0,"high":127}, border_colour=asic_layout_colour)
        # self.asic_load = QValueRangeWidget(name="ASIC load", value=2, condition={"low":2,"high":15}, border_colour=asic_layout_colour)
        # asic_layout.addWidget(self.asic, 0, 0, 1, 2) 
        # asic_layout.addWidget(self.asic_vth, 1, 0, 1, 1) 
        # asic_layout.addWidget(self.asic_dth, 1, 1, 1, 1)
        # asic_layout.addWidget(self.asic_load, 2, 0, 1, 2)
        # ping
        # ping_layout = QtWidgets.QGridLayout()
        # ping_layout_colour = "rgb(213, 105, 48)"
        # self.ping = QValueRangeWidget(name="ping", value=60, condition={"low":2,"high":15}, border_colour=ping_layout_colour)
        # ping_layout.addWidget(self.ping, 0, 0, 1, 2) 

        # self._value_layout.addWidget(self.software_stat) 
        # self._value_layout.addWidget(self.de_mode) 
        self._value_layout.addLayout(de_layout) 

        self._value_layout.addLayout(cts_layout) 
        
        self._value_layout.addLayout(strips_layout) 
        self._value_layout.addLayout(frames_layout)
        # self._value_layout.addLayout(asic_layout)  

        # self._value_layout.addLayout(ping_layout) 
        # self._value_layout.addWidget(self.asic_vth) 
        # self._value_layout.addWidget(self.asic_dth) 
        # self._value_layout.addWidget(self.asic_load) 
        set_all_spacings(self._value_layout)
        # self.somevalue0.setMinimumSize(QtCore.QSize(200,100))
        # self.somevalue1.setMinimumSize(QtCore.QSize(200,100))
        # self.somevalue2.setMinimumSize(QtCore.QSize(200,100))
        # self.somevalue3.setMinimumSize(QtCore.QSize(200,100))
        # self.somevalue4.setMinimumSize(QtCore.QSize(200,100))
        # self.somevalue5.setMinimumSize(QtCore.QSize(200,100))

        self.image.reader.value_changed_collection.connect(self.all_fields)

        ## all widgets together
        # image
        global_layout = QGridLayout()
        # global_layout.addWidget(self.image, 0, 0, 4, 4)
        global_layout.addLayout(image_layout, 0, 0, 4, 4)#,
                                #alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop) # y,x,h,w
        # pedestal
        # global_layout.addWidget(self.ped, 4, 0, 4, 3)
        global_layout.addLayout(ped_layout, 4, 0, 2, 4)#,
                                #alignment=QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)# y,x,h,w
        # status values
        # global_layout.addWidget(self.somevalue0, 0, 4, 1, 1)
        # global_layout.addWidget(self.somevalue1, 1, 4, 1, 1)
        # global_layout.addWidget(self.somevalue2, 2, 4, 1, 1)
        # global_layout.addWidget(self.somevalue3, 3, 4, 1, 1)
        # global_layout.addWidget(self.somevalue4, 4, 4, 1, 1)
        # global_layout.addWidget(self.somevalue5, 5, 4, 1, 1)
        # global_layout.addWidget(self.somevalue5, 6, 4, 1, 1)
        global_layout.addLayout(value_layout, 0, 4, 6, 2)#,
                                #alignment=QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)
        
        # make sure all cell sizes in the grid expand in proportion
        # for col in range(global_layout.columnCount()):
        #     global_layout.setColumnStretch(col, 1)
        # for row in range(global_layout.rowCount()):
        #     global_layout.setRowStretch(row, 1)
        unifrom_layout_stretch(global_layout, grid=True)

        # image_layout.setContentsMargins(0, 0, 0, 0) # left, top, right, bottom
        self._image_layout.setContentsMargins(0, 0, 0, 0) # left, top, right, bottom
        # image_layout.setContentsMargins(0, 0, 0, 0)
        # ped_layout.setContentsMargins(0, 0, 0, 0) # left, top, right, bottom
        self._ped_layout.setContentsMargins(0, 0, 0, 0)
        self._value_layout.setContentsMargins(0, 0, 0, 0)
        self._value_layout.setSpacing(6)
        strips_layout.setSpacing(0)
        frames_layout.setSpacing(0)
        # asic_layout.setSpacing(0)
        de_layout.setSpacing(0)
        cts_layout.setSpacing(0)
        # ping_layout.setSpacing(0)
        global_layout.setHorizontalSpacing(0)
        global_layout.setVerticalSpacing(0)
        global_layout.setContentsMargins(0, 0, 0, 0)

        # actually display the layout
        self.setLayout(global_layout)

    def all_fields(self):
        """ 
        Update the:
        * count rate field, 
        """
        self.cts.update_label(self.image.reader.collection.total_counts())
        self.cts.update_tool_tip({"Ct Now":self.image.reader.collection.total_counts(), 
                                  "Ct Mean":"N/A", 
                                  "Ct Median":"N/A", 
                                  "Ct Max.":"N/A", 
                                  "Ct Min.":"N/A"})

    def layout_bkg(self, main_layout, panel_name, style_sheet_string, grid=False):
        """ Adds a background widget (panel) to a main layout so border, colours, etc. can be controlled. """
        # create panel widget
        self.panels[panel_name] = QtWidgets.QWidget()

        # make the panel take up the main layout 
        main_layout.addWidget(self.panels[panel_name])

        # edit the main layout widget however you like
        self.panels[panel_name].setStyleSheet(style_sheet_string)

        # now return a new, child layout that inherits from the panel widget
        if grid:
            return QtWidgets.QGridLayout(self.panels[panel_name])
        else:
            return QtWidgets.QVBoxLayout(self.panels[panel_name])

    def _layout_style(self, border_colour, background_colour):
        """ Define a global layout style. """
        # return f"border-width: 2px; border-style: outset; border-radius: 10px; border-color: {border_colour}; background-color: {background_colour};"
        return f"border-width: 2px; border-style: outset; border-radius: 0px; border-color: {border_colour}; background-color: {background_colour};"
    
    def update_aspect(self, aspect_ratio):
        """ Update the image aspect ratio (width/height). """
        self.aspect_ratio = aspect_ratio

    def resizeEvent(self,event):
        """ Define how the widget can be resized and keep the same apsect ratio. """
        super().resizeEvent(event)
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        # image_resize = QtCore.QSize(int(event.size().width()*0.6), int(event.size().height()*0.6))
        # self.image.resize(image_resize)
        # ped_resize = QtCore.QSize(int(event.size().width()*0.6), int(event.size().height()*0.4))
        # self.ped.resize(ped_resize)
        if event is None:
            return 
        
        new_size = QtCore.QSize(self.detw, int(self.detw / self.aspect_ratio)) #width, height/(width/height)
        new_size.scale(event.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.resize(new_size)

class AllCdTeView(QWidget):
    def __init__(self, cdte0, cdte1, cdte2, cdte3):
        super().__init__()     
        
        # self.setGeometry(100,100,2000,350)
        self.detw, self.deth = 2000,500
        self.setGeometry(100,100,self.detw, self.deth)
        self.setMinimumSize(600,150)
        self.setWindowTitle("All CdTe View")
        self.aspect_ratio = self.detw/self.deth

        # datafile0 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeTrialsOfParser-20231102/cdte.log"
        # datafile1 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte2.log"
        # datafile2 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte3.log"
        # datafile3 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte4.log"

        f0 = CdTeWidget(data_file=cdte0, name=os.path.basename(cdte0), image_angle=-150)
        # f0.resize(QtCore.QSize(150, 190))
        _f0 =QHBoxLayout()
        _f0.addWidget(f0)

        f1 = CdTeWidget(data_file=cdte1, name=os.path.basename(cdte1), image_angle=-30)
        # f1.resize(QtCore.QSize(150, 150))
        _f1 =QGridLayout()
        _f1.addWidget(f1, 0, 0)

        f2 = CdTeWidget(data_file=cdte2, name=os.path.basename(cdte2), image_angle=-90)
        # f2.resize(QtCore.QSize(150, 150))
        _f2 =QGridLayout()
        _f2.addWidget(f2, 0, 0)

        f3 = CdTeWidget(data_file=cdte3, name=os.path.basename(cdte3), image_angle=+30)
        # f3.resize(QtCore.QSize(150, 150))
        _f3 =QGridLayout()
        _f3.addWidget(f3, 0, 0)

        lay = QGridLayout(spacing=0)
        # w.setStyleSheet("border-width: 2px; border-style: outset; border-radius: 10px; border-color: white; background-color: white;")

        # lay.addWidget(f0, 0, 0, 1, 1)
        # lay.addWidget(f1, 0, 1, 1, 1)
        lay.addLayout(_f0, 0, 0, 1, 1)
        lay.addLayout(_f1, 0, 1, 1, 1)
        lay.addLayout(_f2, 0, 2, 1, 1)
        lay.addLayout(_f3, 0, 3, 1, 1)

        lay.setContentsMargins(2, 2, 2, 2) # left, top, right, bottom
        lay.setHorizontalSpacing(5)
        self.setStyleSheet("border-width: 2px; border-style: outset; border-radius: 10px; border-color: white; background-color: rgba(238, 186, 125, 150);")

        self.setLayout(lay)

    def resizeEvent(self,event):
        """ Define how the widget can be resized and keep the same apsect ratio. """
        super().resizeEvent(event)
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        # image_resize = QtCore.QSize(int(event.size().width()*0.6), int(event.size().height()*0.6))
        # self.image.resize(image_resize)
        # ped_resize = QtCore.QSize(int(event.size().width()*0.6), int(event.size().height()*0.4))
        # self.ped.resize(ped_resize)
        if event is None:
            return 
        
        new_size = QtCore.QSize(self.detw, int(self.detw / self.aspect_ratio)) #width, height/(width/height)
        new_size.scale(event.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.resize(new_size)

if __name__=="__main__":
    app = QApplication([])

    # different data files to try
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeImages/no2022_03/NiFoilAm241/10min/test_20230609a_det03_00012_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/berkeley/prototype_vibe_test/fromBerkeley_postVibeCheckFiles/Am241/test_berk_20230803_proto_Am241_1min_postvibe2_00006_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/berkeley/prototype_vibe_test/fromBerkeley_postVibeCheckFiles/Fe55/test_berk_20230803_proto_Fe55_1min__postvibe2_00008_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeImages/no2021_05/Am241/1min/test_berk_20230728_det05_00005_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeImages/no2021_05/Fe55/1min/test_berk_20230728_det05_00006_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeImages/no2021_05/Cr51/1min/test_berk_20230728_det05_00007_001"
    # datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/berkeley/prototype_vibe_test/vibetest_presinez_berk_20230802_proto_00012_001"
    
    # import os
    # FILE_DIR = os.path.dirname(os.path.realpath(__file__))
    # datafile = FILE_DIR+"/../data/test_berk_20230728_det05_00007_001"
    # datafile = "/Users/kris/Desktop/test_230306_00001_001_nohk"
    # datafile="/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/calibration/j-sideRootData/usingDAQ/raw2root/backgrounds-20230331-newGrounding/20230331_bkg_00001_001"
    # # datafile = "/Users/kris/Desktop/cdte_20231030.log"
    # # datafile = "/Users/kris/Desktop/cdte_20231030_postsend.log"
    # # datafile = "/Users/kris/Desktop/cdte_20231030_presend.log"
    # datafile = "/Users/kris/Desktop/cdte_20231030_fullread.log"
    # datafile = "/Users/kris/Desktop/cdte_src_mod.log"
    # datafile = "/Users/kris/Desktop/gse_mod.log"
    # datafile = "/Users/kris/Desktop/from_de.log"
    # # datafile = "/Users/kris/Desktop/from_gse.log"
    datafile = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeTrialsOfParser-20231102/cdte.log"
    # # datafile = ""

    # # `datafile = FILE_DIR+"/../data/cdte.log"`
    # reader = CdTeFileReader(datafile)#CdTeReader(data_file)
    # # reader = CdTeReader(datafile)
    
    # f0 = CdTeWidget(data_file=datafile)
    # _f0 =QGridLayout()
    # _f0.addWidget(f0, 0, 0)

    # f1 = CdTeWidget(data_file=datafile)
    # _f1 =QGridLayout()
    # _f1.addWidget(f1, 0, 0)

    # f2 = CdTeWidget(data_file=datafile)
    # _f2 =QGridLayout()
    # _f2.addWidget(f2, 0, 0)

    # f3 = CdTeWidget(data_file=datafile)
    # _f3 =QGridLayout()
    # _f3.addWidget(f3, 0, 0)
    
    # w = QWidget()
    # lay = QGridLayout(w)
    # w.setStyleSheet("border-width: 2px; border-style: outset; border-radius: 10px; border-color: white; background-color: white;")

    # # lay.addWidget(f0, 0, 0, 1, 1)
    # # lay.addWidget(f1, 0, 1, 1, 1)
    # lay.addLayout(_f0, 0, 0, 1, 1)
    # lay.addLayout(_f1, 0, 1, 1, 1)
    # lay.addLayout(_f2, 0, 2, 1, 1)
    # lay.addLayout(_f3, 0, 3, 1, 1)

    cdte0 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/CdTeTrialsOfParser-20231102/cdte.log"
    cdte1 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte2.log"
    cdte2 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte3.log"
    cdte3 = "/Users/kris/Documents/umnPostdoc/projects/both/foxsi4/gse/preWSMRship/Jan24-gse_filter/cdte4.log"
    
    # w.resize(1000,500)
    w = AllCdTeView(cdte0, cdte1, cdte2, cdte3)
    # w = CdTeWidget(data_file=datafile)
    
    w.show()
    app.exec()