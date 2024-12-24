import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel, QGraphicsView, QGraphicsScene, QSplitter, QMenu, QLineEdit, QGroupBox, QScrollArea
from PyQt5.QtGui import QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
import math

class GrafoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Red Social Interactiva basada en Grafos')
        self.setGeometry(100, 100, 1000, 700)

        self.nodos = {}
        self.enlaces = []
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        left_panel = self.createLeftPanel()
        right_panel = self.createRightPanel()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)

    def createLeftPanel(self):
        left_panel = QScrollArea()
        left_panel_widget = QWidget()
        left_layout = QVBoxLayout()

        # Aseguramos que el layout del panel izquierdo se alinee hacia arriba
        left_layout.setAlignment(Qt.AlignTop)

        left_layout.addWidget(QLabel('<h3>Opciones del Grafo</h3>'))

        # Botón Ingresar Grafo
        self.iniciarGrafoBtn = QPushButton('Ingresar Grafo', self)
        self.iniciarGrafoBtn.clicked.connect(self.mostrarOpcionesArchivo)
        left_layout.addWidget(self.iniciarGrafoBtn)

        # Botón Guardar Grafo
        self.guardarGrafoBtn = QPushButton('Guardar Grafo', self)
        self.guardarGrafoBtn.clicked.connect(self.mostrarOpcionesGuardar)
        left_layout.addWidget(self.guardarGrafoBtn)

        # Botón Eliminar Grafo
        self.eliminarGrafoBtn = QPushButton('Eliminar Grafo', self)
        self.eliminarGrafoBtn.clicked.connect(self.eliminarGrafo)
        left_layout.addWidget(self.eliminarGrafoBtn)

        # Agregar los grupos de nodos y transiciones
        left_layout.addWidget(self.createNodeGroup())
        left_layout.addWidget(self.createTransitionGroup())

        left_panel_widget.setLayout(left_layout)
        left_panel.setWidget(left_panel_widget)
        left_panel.setWidgetResizable(True)

        return left_panel

    def createNodeGroup(self):
        group_box = QGroupBox('Añadir Nodo')
        layout = QVBoxLayout()

        self.nombreNodoInput = QLineEdit(self)
        self.nombreNodoInput.setPlaceholderText('Nombre del Nodo')
        self.edadNodoInput = QLineEdit(self)
        self.edadNodoInput.setPlaceholderText('Edad del Nodo')
        self.ciudadNodoInput = QLineEdit(self)
        self.ciudadNodoInput.setPlaceholderText('Ciudad del Nodo')
        self.agregarNodoBtn = QPushButton('Agregar Nodo', self)
        self.agregarNodoBtn.clicked.connect(self.agregarNodo)

        layout.addWidget(self.nombreNodoInput)
        layout.addWidget(self.edadNodoInput)
        layout.addWidget(self.ciudadNodoInput)
        layout.addWidget(self.agregarNodoBtn)

        group_box.setLayout(layout)
        return group_box

    def createTransitionGroup(self):
        group_box = QGroupBox('Añadir Transición')
        layout = QVBoxLayout()

        self.nodoDeInput = QLineEdit(self)
        self.nodoDeInput.setPlaceholderText('ID Nodo Origen')
        self.nodoAInput = QLineEdit(self)
        self.nodoAInput.setPlaceholderText('ID Nodo Destino')
        self.agregarTransicionBtn = QPushButton('Agregar Transición', self)
        self.agregarTransicionBtn.clicked.connect(self.agregarTransicion)

        layout.addWidget(self.nodoDeInput)
        layout.addWidget(self.nodoAInput)
        layout.addWidget(self.agregarTransicionBtn)

        group_box.setLayout(layout)
        return group_box

    def createRightPanel(self):
        right_panel = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel('<h3>Visualización de Red Social en Grafos</h3>'))
        self.grafoScene = QGraphicsScene(self)
        self.grafoView = QGraphicsView(self.grafoScene, self)
        layout.addWidget(self.grafoView)

        right_panel.setLayout(layout)
        return right_panel

    def mostrarOpcionesArchivo(self):
        menu = QMenu(self)

        csv_action = menu.addAction("CSV")
        json_action = menu.addAction("JSON")

        csv_action.triggered.connect(self.seleccionarArchivosCSV)
        json_action.triggered.connect(self.cargarArchivoJSON)

        # Calcula la posición global del botón
        boton_rect = self.iniciarGrafoBtn.rect()
        posicion_global = self.iniciarGrafoBtn.mapToGlobal(boton_rect.bottomLeft())

        # Muestra el menú en la posición calculada
        menu.exec_(posicion_global)


    def seleccionarArchivosCSV(self):
        nodos_csv, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV de nodos", "", "CSV Files (*.csv)")
        transiciones_csv, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV de transiciones", "", "CSV Files (*.csv)")

        if nodos_csv and transiciones_csv:
            self.cargarArchivoCSV(nodos_csv, transiciones_csv)

    def cargarArchivoCSV(self, nodos_csv, transiciones_csv):
        with open(nodos_csv, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.nodos[int(row['id'])] = row

        with open(transiciones_csv, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.enlaces.append((int(row['de']), int(row['a'])))

        self.dibujarGrafo()

    def cargarArchivoJSON(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo JSON", "", "JSON Files (*.json)")

        if archivo:
            with open(archivo, 'r', encoding='utf-8') as file:
                datos = json.load(file)

            self.nodos = {nodo['id']: nodo for nodo in datos['nodos']}
            self.enlaces = [(trans['de'], trans['a']) for trans in datos['transiciones']]

            self.dibujarGrafo()

    def agregarNodo(self):
        nombre = self.nombreNodoInput.text()
        edad = self.edadNodoInput.text()
        ciudad = self.ciudadNodoInput.text()

        if not nombre or not edad or not ciudad:
            return

        nuevo_id = max(self.nodos.keys(), default=0) + 1
        self.nodos[nuevo_id] = {'id': nuevo_id, 'nombre': nombre, 'edad': int(edad), 'ciudad': ciudad}

        self.nombreNodoInput.clear()
        self.edadNodoInput.clear()
        self.ciudadNodoInput.clear()

        self.dibujarGrafo()

    def agregarTransicion(self):
        try:
            nodo_de = int(self.nodoDeInput.text())
            nodo_a = int(self.nodoAInput.text())
        except ValueError:
            return

        if nodo_de in self.nodos and nodo_a in self.nodos:
            self.enlaces.append((nodo_de, nodo_a))
            self.nodoDeInput.clear()
            self.nodoAInput.clear()

            self.dibujarGrafo()

    def mostrarOpcionesGuardar(self):
        menu = QMenu(self)

        csv_action = menu.addAction("CSV")
        json_action = menu.addAction("JSON")

        csv_action.triggered.connect(self.guardarComoCSV)
        json_action.triggered.connect(self.guardarComoJSON)
        
        boton_rect = self.guardarGrafoBtn.rect()
        posicion_global = self.guardarGrafoBtn.mapToGlobal(boton_rect.bottomLeft())

        # Muestra el menú en la posición calculada
        menu.exec_(posicion_global)
    def guardarComoCSV(self):
        nodos_csv, _ = QFileDialog.getSaveFileName(self, "Guardar nodos como CSV", "", "CSV Files (*.csv)")
        transiciones_csv, _ = QFileDialog.getSaveFileName(self, "Guardar transiciones como CSV", "", "CSV Files (*.csv)")

        if nodos_csv and transiciones_csv:
            with open(nodos_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'nombre', 'edad', 'ciudad'])
                writer.writeheader()
                for nodo in self.nodos.values():
                    writer.writerow(nodo)

            with open(transiciones_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['de', 'a'])
                writer.writerows(self.enlaces)
    def guardarComoJSON(self):
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar como JSON", "", "JSON Files (*.json)")

        if archivo:
            datos = {
                "nodos": list(self.nodos.values()),
                "transiciones": [{"de": enlace[0], "a": enlace[1]} for enlace in self.enlaces]
            }
            with open(archivo, 'w', encoding='utf-8') as file:
                json.dump(datos, file, ensure_ascii=False, indent=4)


    def dibujarGrafo(self):
        self.grafoScene.clear()

        posicion_nodos = {}
        radio_nodo = 20
        espacio_entre_circulos = 100  # Espacio entre círculos concéntricos
        radio_inicial = 50  # Radio del primer círculo (nodo central)
        centro_x, centro_y = 400, 300  # Coordenadas del centro del grafo

        # Colores y estilos
        color_nodo_central = QColor("#ff6347")  # Rojo tecnológico (tomate)
        color_nodo_secundario = QColor("#1e90ff")  # Azul tecnológico
        color_texto = QColor("#dcdcdc")  # Texto en gris claro
        color_linea = QColor("#32cd32")  # Verde lima para las líneas
        fuente_texto = QFont("Arial", 8, QFont.Bold)

        # Obtener los nodos
        nodos = list(self.nodos.items())

        # El primer nodo será el nodo central
        if nodos:
            id_nodo_central, datos_central = nodos[0]
            circulo_central = QGraphicsEllipseItem(
                centro_x - radio_nodo / 2, 
                centro_y - radio_nodo / 2, 
                radio_nodo, 
                radio_nodo
            )
            circulo_central.setBrush(QBrush(color_nodo_central))  # Nodo central en rojo tecnológico
            self.grafoScene.addItem(circulo_central)

            texto_central = self.grafoScene.addText(f"{datos_central['nombre']}\nID: {id_nodo_central}")
            texto_central.setDefaultTextColor(color_texto)
            texto_central.setFont(fuente_texto)
            texto_central.setPos(centro_x - 30, centro_y - 30)
            posicion_nodos[id_nodo_central] = (centro_x, centro_y)

        # Nodos restantes
        for idx, (id_nodo, datos) in enumerate(nodos[1:], start=1):
            # Calcular el círculo en el que se encuentra este nodo
            nivel = 1  # Primer círculo
            while idx >= nivel * 6:
                idx -= nivel * 6
                nivel += 1

            # Calcular la posición angular del nodo
            angulo = 2 * math.pi / (nivel * 6) * idx
            radio_actual = radio_inicial + espacio_entre_circulos * (nivel - 1)
            x = centro_x + radio_actual * math.cos(angulo)
            y = centro_y + radio_actual * math.sin(angulo)

            # Dibujar nodo
            circulo = QGraphicsEllipseItem(x - radio_nodo / 2, y - radio_nodo / 2, radio_nodo, radio_nodo)
            circulo.setBrush(QBrush(color_nodo_secundario))  # Nodo secundario en azul tecnológico
            self.grafoScene.addItem(circulo)

            texto = self.grafoScene.addText(f"{datos['nombre']}\nID: {id_nodo}")
            texto.setDefaultTextColor(color_texto)
            texto.setFont(fuente_texto)
            texto.setPos(x - 30, y - 30)

            posicion_nodos[id_nodo] = (x, y)

        # Dibujar enlaces
        for de, a in self.enlaces:
            if de in posicion_nodos and a in posicion_nodos:
                x1, y1 = posicion_nodos[de]
                x2, y2 = posicion_nodos[a]
                linea = QGraphicsLineItem(x1, y1, x2, y2)
                linea.setPen(QPen(color_linea, 2))  # Línea en verde lima
                self.grafoScene.addItem(linea)


    def eliminarGrafo(self):
        confirm = QMessageBox.question(
            self, 'Confirmar Eliminación',
            '¿Está seguro de que desea eliminar todo el grafo?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.nodos.clear()
            self.enlaces.clear()
            QMessageBox.information(self, "Grafo Eliminado", "El grafo ha sido eliminado correctamente.")
            self.dibujarGrafo()

def aplicarTemaOscuro(app):
    estilo_oscuro = """
    QWidget {
        background-color: #1e1e1e;
        color: #dcdcdc;
        font-family: Arial;
    }
    QGraphicsView {
        border: 1px solid #444;
        background-color: #2d2d2d;
    }
    QPushButton {
        background-color: #3a3a3a;
        color: #dcdcdc;
        border: 1px solid #555;
        border-radius: 5px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #505050;
    }
    QPushButton:pressed {
        background-color: #6a6a6a;
    }
    QLineEdit {
        background-color: #2a2a2a;
        color: #dcdcdc;
        border: 1px solid #555;
        border-radius: 3px;
        padding: 2px;
    }
    QLabel {
        color: #dcdcdc;
    }
    QGraphicsEllipseItem {
        background-color: #007acc;  /* Azul tecnológico */
    }
    """
    app.setStyleSheet(estilo_oscuro)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Llamar la función para aplicar el tema oscuro
    aplicarTemaOscuro(app)

    # Mostrar la ventana principal
    window = GrafoApp()
    window.show()

    sys.exit(app.exec_())

