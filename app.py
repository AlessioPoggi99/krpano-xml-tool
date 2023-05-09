'''
    @Author: Alessio Poggi
    @Date: 04/05/2023
    @Version: 1.0.0
    @Email: alessio_poggi@hotmail.it
    @Status: Production
'''

import sys, time, os, shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from datetime import datetime

VERSION = '1.0.0'
BUTTON_EMPTY_TEXT = '. . .'
POSITIONS = ('lefttop', 'left', 'leftbottom', 'top', 'center', 'bottom', 'righttop', 'right', 'rightbottom')

class Window(QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        layout = QVBoxLayout()

        # XML selector
        self.projectLayout = QVBoxLayout()
        self.projectBtn = QPushButton(BUTTON_EMPTY_TEXT)
        self.projectBtn.clicked.connect(self.getdir)
        self.projectLayout.addWidget(QLabel("Select existing krpano project directory"))
        self.projectLayout.addWidget(self.projectBtn)

        # Startup scene
        self.startSceneLayout = QHBoxLayout()
        self.startSceneCb = QCheckBox("Set startup scene name")
        self.startSceneName = QLineEdit()
        self.startSceneCb.toggled.connect(lambda checked: self.startSceneName.setEnabled(True) if checked else self.startSceneName.setEnabled(False))
        self.startSceneLayout.addWidget(self.startSceneCb)
        self.startSceneLayout.addStretch()
        self.startSceneLayout.addWidget(self.startSceneName)

        # Logo checkbox
        self.logoCb = QCheckBox("Add logo", self)
        self.logoCb.toggled.connect(lambda checked: [lw.setEnabled(True) for lw in self.logoWidgets] if checked else [lw.setEnabled(False) for lw in self.logoWidgets])
        self.logoLayout = QVBoxLayout()
        self.logoLayout.setContentsMargins(25, 0, 0, 0)
        # Logo image selector
        self.logoSelectLayout = QHBoxLayout()
        self.logoSelectLabel = QLabel("Logo image:")
        self.logoImageBtn = QPushButton(BUTTON_EMPTY_TEXT)
        self.logoImageBtn.clicked.connect(lambda: self.getfile(self.logoImageBtn, "Image files (*.png *.jpg *.jpeg *.svg)"))
        self.logoSelectLayout.addWidget(self.logoSelectLabel)
        self.logoSelectLayout.addWidget(self.logoImageBtn, 1)
        self.logoLayout.addLayout(self.logoSelectLayout)
        # Logo position radio buttons
        self.logoPositionLayout = QHBoxLayout()
        self.logoPositionLabel = QLabel("Logo position:")
        self.logoPositionLayout.addWidget(self.logoPositionLabel)
        self.logoPositionCb = QComboBox()
        self.logoPositionCb.addItems(POSITIONS)
        self.logoPositionCb.setCurrentIndex(6)
        self.logoPositionLayout.addWidget(self.logoPositionCb)
        self.logoLayout.addLayout(self.logoPositionLayout)
        # Logo scale spin box
        self.logoScaleLayout = QHBoxLayout()
        self.logoScaleLabel = QLabel("Logo scale:")
        self.logoScaleLayout.addWidget(self.logoScaleLabel)
        self.logoScaleSb = QDoubleSpinBox()
        self.logoScaleSb.setRange(0.01, 100.)
        self.logoScaleSb.setValue(0.5)
        self.logoScaleSb.setSingleStep(0.1)
        self.logoScaleLayout.addWidget(self.logoScaleSb)
        self.logoLayout.addLayout(self.logoScaleLayout)

        # Mini map checkbox
        self.mapCb = QCheckBox("Add mini map", self)
        self.mapCb.toggled.connect(lambda checked: [mw.setEnabled(True) for mw in self.mapWidgets] if checked else [mw.setEnabled(False) for mw in self.mapWidgets])
        self.mapLayout = QVBoxLayout()
        self.mapLayout.setContentsMargins(25, 0, 0, 0)
        # Mini map image selector
        self.mapSelectLayout = QHBoxLayout()
        self.mapSelectLabel = QLabel("Map image:")
        self.mapImageBtn = QPushButton(BUTTON_EMPTY_TEXT)
        self.mapImageBtn.clicked.connect(lambda: self.getfile(self.mapImageBtn, "Image files (*.png *.jpg *.jpeg *.svg)"))
        self.mapSelectLayout.addWidget(self.mapSelectLabel)
        self.mapSelectLayout.addWidget(self.mapImageBtn, 1)
        self.mapLayout.addLayout(self.mapSelectLayout)
        # Mini map position radio buttons
        self.mapPositionLayout = QHBoxLayout()
        self.mapPosiotionLabel = QLabel("Map position:")
        self.mapPositionLayout.addWidget(self.mapPosiotionLabel)
        self.mapPositionCb = QComboBox()
        self.mapPositionCb.addItems(POSITIONS)
        self.mapPositionCb.setCurrentIndex(2)
        self.mapPositionLayout.addWidget(self.mapPositionCb)
        self.mapLayout.addLayout(self.mapPositionLayout)
        # Mini map open and closed scales spin box
        self.mapScaleLayout = QHBoxLayout()
        self.mapCloseScaleLabel = QLabel("Closed map scale:")
        self.mapScaleLayout.addWidget(self.mapCloseScaleLabel)
        self.closeMapScaleSb = QDoubleSpinBox()
        self.closeMapScaleSb.setRange(0.01, 100.)
        self.closeMapScaleSb.setValue(0.5)
        self.closeMapScaleSb.setSingleStep(0.1)
        self.mapScaleLayout.addWidget(self.closeMapScaleSb)
        self.mapOpenScaleLabel = QLabel("Open map scale:")
        self.mapScaleLayout.addWidget(self.mapOpenScaleLabel)
        self.openMapScaleSb = QDoubleSpinBox()
        self.openMapScaleSb.setRange(0.01, 100.)
        self.openMapScaleSb.setValue(1)
        self.openMapScaleSb.setSingleStep(0.1)
        self.mapScaleLayout.addWidget(self.openMapScaleSb)
        self.mapLayout.addLayout(self.mapScaleLayout)

        # Hotspot checkbox
        self.hotspotCb = QCheckBox("Add hotspots", self)
        self.hotspotCb.toggled.connect(lambda checked: [hw.setEnabled(True) for hw in self.hotspotWidgets] if checked else [hw.setEnabled(False) for hw in self.hotspotWidgets])
        self.hotspotLayout = QVBoxLayout()
        self.hotspotLayout.setContentsMargins(50, 0, 0, 0)
        # Coordinate file selector
        self.coordinatesSelectLayout = QHBoxLayout()
        self.coordinatesSelectLabel = QLabel("Coordinates file:")
        self.coordinatesBtn = QPushButton(BUTTON_EMPTY_TEXT)
        self.coordinatesBtn.clicked.connect(lambda: self.getfile(self.coordinatesBtn, "Text files (*.txt)"))
        self.coordinatesSelectLayout.addWidget(self.coordinatesSelectLabel)
        self.coordinatesSelectLayout.addWidget(self.coordinatesBtn, 1)
        self.hotspotLayout.addLayout(self.coordinatesSelectLayout)
        # Hotspot scale spin box
        self.hotspotScaleLayout = QHBoxLayout()
        self.hotspotScaleLabel = QLabel("Hotspot scale:")
        self.hotspotScaleLayout.addWidget(self.hotspotScaleLabel)
        self.hotspotScaleSb = QDoubleSpinBox()
        self.hotspotScaleSb.setRange(0.01, 100.)
        self.hotspotScaleSb.setValue(0.3)
        self.hotspotScaleSb.setSingleStep(0.1)
        self.hotspotScaleLayout.addWidget(self.hotspotScaleSb)
        self.hotspotLayout.addLayout(self.hotspotScaleLayout)
        #
        self.mapLayout.addWidget(self.hotspotCb)
        self.mapLayout.addLayout(self.hotspotLayout)

        # Radar checkbox
        self.radarCb = QCheckBox("Add radar", self)
        self.radarCb.toggled.connect(lambda checked: [rw.setEnabled(True) for rw in self.radarWidgets] if checked else [rw.setEnabled(False) for rw in self.radarWidgets])
        self.radarLayout = QHBoxLayout()
        # Radar scale spin box
        self.radarScaleLayout = QHBoxLayout()
        self.radarScaleLayout.setContentsMargins(50, 0, 0, 0)
        self.radarScaleLabel = QLabel("Radar scale:")
        self.radarScaleLayout.addWidget(self.radarScaleLabel)
        self.radarScaleSb = QDoubleSpinBox()
        self.radarScaleSb.setRange(0.01, 100.)
        self.radarScaleSb.setValue(0.3)
        self.radarScaleSb.setSingleStep(0.1)
        self.radarScaleLayout.addWidget(self.radarScaleSb)
        #
        self.mapLayout.addWidget(self.radarCb)
        self.mapLayout.addLayout(self.radarScaleLayout)

        # Generate button and plain text for logs
        self.generateBtn = QPushButton("Generate XML")
        self.generateBtn.setStyleSheet(
            "padding: 10px 0px; margin-top: 30px; font-weight: bold;"
        )
        self.generateBtn.clicked.connect(self.generateXML)
        self.generateBtn.setEnabled(False)
        self.logTextEdit = QPlainTextEdit()
        font = self.logTextEdit.font()
        font.setPointSize(10)
        self.logTextEdit.setFont(font)
        self.logTextEdit.font().setPointSize(10)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setEnabled(False)

        self.checkBoxArr = [self.startSceneCb, self.logoCb, self.mapCb]
        self.logoWidgets = [self.logoSelectLabel, self.logoImageBtn, self.logoPositionLabel, self.logoPositionCb, self.logoScaleLabel, self.logoScaleSb]
        self.mapWidgets = [self.mapSelectLabel, self.mapImageBtn, self.mapPosiotionLabel, self.mapPositionCb, self.mapOpenScaleLabel, self.openMapScaleSb, self.mapCloseScaleLabel, self.closeMapScaleSb, self.hotspotCb, self.radarCb]
        self.hotspotWidgets = [self.coordinatesSelectLabel, self.coordinatesBtn, self.hotspotScaleLabel, self.hotspotScaleSb]
        self.radarWidgets = [self.radarScaleLabel, self.radarScaleSb]
        self.generateWidgets = [self.generateBtn, self.logTextEdit]

        self.copyrightLayout = QHBoxLayout()
        self.copyrightLabel = QLabel("2023 v{} - Alessio Poggi".format(VERSION))
        self.copyrightLabel.setStyleSheet(
            "margin-top: 15px; color: gray; font-size: 10px;"
        )
        self.copyrightLayout.addStretch()
        self.copyrightLayout.addWidget(self.copyrightLabel)
        self.copyrightLayout.addStretch()

        layout.setContentsMargins(20, 20, 20, 5)
        layout.addLayout(self.projectLayout)
        layout.addLayout(self.startSceneLayout)
        layout.addWidget(self.logoCb)
        layout.addLayout(self.logoLayout)
        layout.addWidget(self.mapCb)
        layout.addLayout(self.mapLayout)
        layout.addWidget(self.generateBtn)
        layout.addWidget(self.logTextEdit)
        layout.addLayout(self.copyrightLayout)
        self.setLayout(layout)
        self.disableAll()

    def disableAll(self):
        for cb in self.checkBoxArr:
            cb.setEnabled(False)
        for lw in self.logoWidgets:
            lw.setEnabled(False)
        for mw in self.mapWidgets:
            mw.setEnabled(False)
        for hw in self.hotspotWidgets:
            hw.setEnabled(False)
        for rw in self.radarWidgets:
            rw.setEnabled(False)
        self.startSceneName.setEnabled(False)
      
    def getdir(self):
        dname = QFileDialog.getExistingDirectory(self, 'Select folder', 'c:\\')
        if dname:
            self.projectBtn.setText(dname)
            for gw in self.generateWidgets:
                    gw.setEnabled(True)
            for cb in self.checkBoxArr:
                cb.setEnabled(True)
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def getfile(self, widget, extension):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', extension)
        if fname:
            widget.setText(fname)

    def appendToKrpano(self, soup, tag):
        try:
            soup.find('krpano').append(tag)
        except:
            self.logTextEdit.appendPlainText("ERROR: It seems that file tour.xml doen't contain 'krpano' tag")

    def generateXML(self):
        self.logTextEdit.clear()

        self.logTextEdit.appendPlainText("Running - {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        
        # Get the start time
        st = time.time()
        
        # Read XML file
        try:
            with open('{}/tour.xml'.format(self.projectBtn.text()), 'r') as f:
                xml_data = f.read()
            soup = BeautifulSoup(xml_data, "lxml")
        except:
            self.logTextEdit.appendPlainText("ERROR: Unable to open or read tour.xml file...\nCheck tour.xml exists inside selected project folder.")
            return
        
        # Create needed directories
        os.makedirs(os.path.dirname('{}/skin/'.format(self.projectBtn.text())), exist_ok=True)
        os.makedirs(os.path.dirname('{}/plugins/'.format(self.projectBtn.text())), exist_ok=True)

        # Add startup scene
        if self.startSceneCb.isChecked():
            startup_scene_name = self.startSceneName.text()
            if startup_scene_name == '':
                self.logTextEdit.appendPlainText("ERROR: Set a startup scene name or deselect the checkbox and try again...")
                return
            action_tag = soup.new_tag('action', name="startup", autorun="onstart")
            action_tag.string = 'loadscene({}, null, MERGE);'.format(startup_scene_name if 'scene_' in startup_scene_name else 'scene_{}'.format(startup_scene_name))
            #soup.find('krpano').append(action_tag)
            self.appendToKrpano(soup, action_tag)
        
        # Add LOGO
        if self.logoCb.isChecked():
            logo_name = self.logoImageBtn.text()
            if logo_name == BUTTON_EMPTY_TEXT:
                self.logTextEdit.appendPlainText("ERROR: Select a logo image or deselect 'add logo' checkbox and try again...")
                return
            shutil.copy(logo_name, '{}/skin/'.format(self.projectBtn.text()))
            layer_tag = soup.new_tag('layer', align="{}".format(self.logoPositionCb.currentText()), capture="false", handcursor="false", keep="true", name="logo", scale="{}".format(self.logoScaleSb.value()), scalechildren="true", url="skin/{}".format(logo_name.rsplit('/', 1)[-1]), y="10", x="10")
            #soup.find('krpano').append(layer_tag)
            self.appendToKrpano(soup, layer_tag)

        # Add MAP
        if self.mapCb.isChecked():
            map_name = self.mapImageBtn.text()
            if map_name == BUTTON_EMPTY_TEXT:
                self.logTextEdit.appendPlainText("ERROR: Select a map image or deselect 'add map' checkbox and try again...")
                return

            shutil.copy(map_name, '{}/skin/'.format(self.projectBtn.text()))
            layer_tag = soup.new_tag('layer', name='map', url="skin/{}".format(map_name.rsplit('/', 1)[-1]), keep='true', handcursor='false', capture='false', align="{}".format(self.mapPositionCb.currentText()), scale="{}".format(self.closeMapScaleSb.value()), scalechildren="true", onclick="openmap();")
            action_tag1 = soup.new_tag('action', name='openmap')
            action_tag1.string = 'set(layer[map].onclick, closemap(); );layer[map].changealign(center,center);set(bigscale,{});if(layer[map].sourcewidth GT stagewidth, bigscale = stagewidth / layer[map].sourcewidth; );tween(layer[map].x, 0);tween(layer[map].y, 0);tween(layer[map].scale, get(bigscale));'.format(self.openMapScaleSb.value())
            action_tag2 = soup.new_tag('action', name='closemap')
            action_tag2.string = 'set(layer[map].onclick, openmap(); );layer[map].changealign({},{});tween(layer[map].x, 0);tween(layer[map].y, 0);tween(layer[map].scale, {});'.format(self.mapPositionCb.currentText(), self.mapPositionCb.currentText(), self.closeMapScaleSb.value())
            #soup.find('krpano').append(layer_tag)
            #soup.find('krpano').append(action_tag1)
            #soup.find('krpano').append(action_tag2)
            self.appendToKrpano(soup, layer_tag)
            self.appendToKrpano(soup, action_tag1)
            self.appendToKrpano(soup, action_tag2)


            # Add HOTSPOTS
            if self.hotspotCb.isChecked():
                if self.coordinatesBtn.text() == BUTTON_EMPTY_TEXT:
                    self.logTextEdit.appendPlainText("ERROR: Select coordinates text file or deselect 'add hotspots' checkbox and try again...")
                    return

                try:
                    with open(self.coordinatesBtn.text(), 'r') as f:
                        coordinates_list = [line.strip().split(',') for line in f]
                except:
                    self.logTextEdit.appendPlainText('ERROR: Unable to read coordinates text file... try again.')
                
                shutil.copy(self.resource_path('assets/gray_circle.png'), '{}/skin/spot.png'.format(self.projectBtn.text()))
                shutil.copy(self.resource_path('assets/red_circle.png'), '{}/skin/active-spot.png'.format(self.projectBtn.text()))
                style_tag = soup.new_tag('style', name="mapspot", scale="{}".format(self.hotspotScaleSb.value()), keep="true", url="skin/spot.png", parent="map", align="lefttop", edge="center")
                style_tag['scale.mobile'] = "2"
                layer_tag = soup.new_tag('layer', name="activespot", scale="{}".format(self.hotspotScaleSb.value()), url="skin/active-spot.png", keep="true", align="lefttop", zorder="2")
                action_tag = soup.new_tag('action', name="mapspot_loadscene")
                action_tag.string = "if(layer[map].scale GT 0.3,set(layer[map].enabled, false);tween(layer[map].alpha, 0.0, 0.3, default,loadscene(%1, null, MERGE, BLEND(1));set(layer[map].onclick, openmap(););layer[map].changealign({},{});set(layer[map].x, 0);set(layer[map].y, 0);set(layer[map].scale, {});set(events[sceneload].onloadcomplete,delayedcall(1,tween(layer[map].alpha, 1.0, 0.5, default, set(layer[map].enabled, true); ););););,loadscene(%1, null, MERGE, BLEND(1)););".format(self.mapPositionCb.currentText(), self.mapPositionCb.currentText(), self.closeMapScaleSb.value())
                #soup.find('krpano').append(style_tag)
                #soup.find('krpano').append(layer_tag)
                #soup.find('krpano').append(action_tag)
                self.appendToKrpano(soup, style_tag)
                self.appendToKrpano(soup, layer_tag)
                self.appendToKrpano(soup, action_tag)


                counter = 1
                for coordinate in coordinates_list:
                    scene_name = 'scene_{}'.format(coordinate[0])
                    layer_tag = soup.new_tag('layer', name='spot{}'.format(counter), style='mapspot', x='{}'.format(coordinate[1]), y='{}'.format(coordinate[2]), zorder='1', onclick='mapspot_loadscene({});'.format(scene_name))
                    #soup.find('krpano').append(layer_tag)
                    self.appendToKrpano(soup, layer_tag)
                    try:
                        for tag in soup.find_all('scene', {'name': scene_name}):
                            tag['onstart'] = 'updateradar();'
                            hlookat = tag.find('view').get('hlookat')
                            radar_angle = round(-float(hlookat) - 90.0, 3)
                            action_tag = soup.new_tag('action', name='updateradar')
                            action_tag.string = 'set(layer[radar].parent, spot{});\nset(layer[activespot].parent, spot{});\nset(plugin[radar].heading, {});'.format(counter, counter, radar_angle)
                            tag.append(action_tag)
                    except:
                        self.logTextEdit.appendPlainText("ERROR: It seems that tour.xml doesn't contain scenes or it does not contain {} scene".format(scene_name))
                    counter += 1
            
                self.logTextEdit.appendPlainText('Succesfully added {} hotspots on the map'.format(counter-1))
                self.logTextEdit.appendPlainText("If hotspots don't work check your coordinate text file formatting [SCENE_NAME,X_COORD,Y_COORD]")

            # Add RADAR
            if self.radarCb.isChecked():
                shutil.copy(self.resource_path('assets/radar.js'), '{}/plugins/radar.js'.format(self.projectBtn.text()))
                layer_tag = soup.new_tag('layer', name="radar", keep="true", url="%VIEWER%/plugins/radar.js", align="center", zorder="1", fillalpha="0.5", fillcolor="0x7F5F3F", linewidth="1.0", linecolor="0xE0E0A0", linealpha="0.5", scale="{}".format(self.radarScaleSb.value()))
                layer_tag['scale.mobile'] = "1.5"
                #soup.find('krpano').append(layer_tag)
                self.appendToKrpano(soup, layer_tag)


        # Save XML, removing html/body/p tags due lxml parser (lxml parser is the only one working on windows)
        try:
            with open("{}/output.xml".format(self.projectBtn.text()), "w") as f:
                #f.write(soup.prettify())
                f.write(soup.find('krpano').prettify())
            self.logTextEdit.appendPlainText('New xml file has been saved as output.xml')
        except:
            self.logTextEdit.appendPlainText('ERROR: Unable to save new xml file... try again.')
            return

        # Get the end time
        et = time.time()
        # get the execution time
        elapsed_time = et - st # *1000 to get milliseconds or /60 to geet minutes
        self.logTextEdit.appendPlainText('Execution time: {} seconds'.format(round(elapsed_time, 2)))

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("KrPano - XML tool")
        self.setMinimumWidth(600)

        self.w = Window()
        self.setCentralWidget(self.w)

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow() #Window()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()