from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QMessageBox, QFormLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import Qt

from src.conexion import conexion


class EditarInformacionPersonalWidget(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Contenedor de contenido alineado arriba
        contenido = QWidget()
        contenido_layout = QVBoxLayout()
        contenido.setLayout(contenido_layout)
        contenido.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Título
        titulo = QLabel("Editar Información Personal")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        contenido_layout.addWidget(titulo)

        # Formulario
        form_layout = QFormLayout()
        self.input_correo = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_direccion = QLineEdit()

        form_layout.addRow("Correo:", self.input_correo)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Dirección:", self.input_direccion)
        contenido_layout.addLayout(form_layout)

        # Botón de guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.actualizar_informacion)
        contenido_layout.addWidget(self.btn_guardar)

        # Añadir contenido al layout principal alineado arriba
        layout.addWidget(contenido, alignment=Qt.AlignTop)

        # Tabla para mostrar la información del cliente
        self.tabla_cliente = QTableWidget()
        self.tabla_cliente.setColumnCount(6)
        self.tabla_cliente.setHorizontalHeaderLabels([
            "Nombre", "Documento", "Correo", "Teléfono", "Dirección", "Estado"
        ])
        self.tabla_cliente.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla_cliente)

        self.setLayout(layout)

        # Cargar los datos del cliente
        self.cargar_datos()
        self.cargar_tabla_cliente()

    def cargar_datos(self):
        try:
            conn = conexion.conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT correo, telefono, direccion
                    FROM Cliente
                    WHERE id_cliente = ?
                """, (self.id_cliente,))
                datos = cursor.fetchone()
                conn.close()

                if datos:
                    self.input_correo.setText(datos[0])
                    self.input_telefono.setText(datos[1] or "")
                    self.input_direccion.setText(datos[2] or "")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la información:\n{e}")

    def actualizar_informacion(self):
        nuevo_correo = self.input_correo.text().strip()
        nuevo_telefono = self.input_telefono.text().strip()
        nueva_direccion = self.input_direccion.text().strip()

        if not nuevo_correo:
            QMessageBox.warning(self, "Campo requerido", "El correo no puede estar vacío.")
            return

        try:
            conn = conexion.conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Cliente
                    SET correo = ?, telefono = ?, direccion = ?
                    WHERE id_cliente = ?
                """, (nuevo_correo, nuevo_telefono, nueva_direccion, self.id_cliente))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Actualización exitosa", "Tu información ha sido actualizada.")
                self.cargar_tabla_cliente()  # Actualizar la tabla después de guardar
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la información:\n{e}")

    def cargar_tabla_cliente(self):
        try:
            conn = conexion.conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nombre, documento, correo, telefono, direccion, estado
                    FROM Cliente
                    WHERE id_cliente = ?
                """, (self.id_cliente,))
                datos = cursor.fetchone()
                conn.close()

                self.tabla_cliente.setRowCount(0)  # Limpiar tabla

                if datos:
                    self.tabla_cliente.setRowCount(1)
                    for col, valor in enumerate(datos):
                        item = QTableWidgetItem(str(valor) if valor is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # No editable
                        self.tabla_cliente.setItem(0, col, item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla del cliente:\n{e}")
