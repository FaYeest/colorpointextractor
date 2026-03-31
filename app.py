from __future__ import annotations

import colorsys
import csv
import sys
import traceback
from collections import Counter
from pathlib import Path
from typing import Iterable, cast

from PIL import Image
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QObject,
    QRectF,
    QSettings,
    QSize,
    QThread,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QImage,
    QKeySequence,
    QMouseEvent,
    QPainter,
    QPen,
    QPixmap,
    QResizeEvent,
    QShortcut,
    QWheelEvent,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QFrame,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QComboBox,
    QSplitter,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


MAC_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                stop: 0 #eef2f7, stop: 1 #dde4ed);
}

QWidget {
    color: #1e1f25;
    font-family: "SF Pro Text", "Helvetica Neue", "Segoe UI";
    font-size: 13px;
}

QFrame#Card {
    background-color: rgba(255, 255, 255, 0.94);
    border: 1px solid rgba(60, 60, 67, 0.12);
    border-radius: 16px;
}

QFrame#ImageSurface {
    background-color: #f8fafc;
    border: 1px solid rgba(60, 60, 67, 0.12);
    border-radius: 12px;
}

QLabel#Title {
    font-size: 25px;
    font-weight: 700;
    color: #14161b;
}

QLabel#Subtitle {
    font-size: 13px;
    color: #5f6470;
}

QLabel#FieldName {
    font-size: 12px;
    color: #6b7280;
}

QLabel#FieldValue {
    font-size: 14px;
    font-weight: 600;
    color: #111827;
}

QLabel#Note {
    color: #5f6470;
    font-size: 12px;
}

QFrame#TopControls {
    background-color: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(60, 60, 67, 0.1);
    border-radius: 14px;
}

QPushButton {
    background-color: #0a84ff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #187ff0;
}

QPushButton:pressed {
    background-color: #0b6ed2;
}

QPushButton:disabled {
    background-color: #bcc6d6;
    color: #f7f9fc;
}

QPushButton#SecondaryButton {
    background-color: #e9edf4;
    color: #1f2937;
}

QPushButton#SecondaryButton:hover {
    background-color: #dbe2ec;
}

QPushButton#ToolbarButton {
    background-color: transparent;
    color: #374151;
    border: 1px solid rgba(60, 60, 67, 0.18);
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: 600;
}

QPushButton#ToolbarButton:hover {
    background-color: rgba(60, 60, 67, 0.08);
}

QPushButton#ToolbarButton:pressed {
    background-color: rgba(60, 60, 67, 0.14);
}

QPushButton#ToolbarButton:disabled {
    color: #9ca3af;
    border: 1px solid rgba(60, 60, 67, 0.12);
    background-color: transparent;
}

QPushButton#ToolbarIcon {
    background-color: transparent;
    color: #374151;
    border: 1px solid rgba(60, 60, 67, 0.18);
    border-radius: 8px;
    padding: 0px;
    font-weight: 700;
}

QPushButton#ToolbarIcon:hover {
    background-color: rgba(60, 60, 67, 0.08);
}

QPushButton#ToolbarIcon:pressed {
    background-color: rgba(60, 60, 67, 0.14);
}

QGraphicsView {
    border: none;
    background: transparent;
}

QSplitter::handle {
    background: transparent;
}

QSplitter::handle:horizontal {
    width: 12px;
    margin: 24px 2px;
    border-radius: 6px;
}

QSplitter::handle:horizontal:hover {
    background: rgba(120, 129, 143, 0.2);
}

QSplitter::handle:horizontal:pressed {
    background: rgba(10, 132, 255, 0.28);
}

QTabWidget::pane {
    border: 1px solid rgba(60, 60, 67, 0.12);
    border-radius: 12px;
    background-color: rgba(255, 255, 255, 0.92);
    top: -1px;
}

QTabBar::tab {
    background: #e8edf5;
    color: #4a5161;
    padding: 7px 12px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #111827;
}

QComboBox {
    background-color: #e9edf4;
    color: #1f2937;
    border: 1px solid rgba(60, 60, 67, 0.14);
    border-radius: 10px;
    padding: 6px 10px;
    min-width: 220px;
}

QComboBox:hover {
    background-color: #dbe2ec;
}

QComboBox::drop-down {
    border: none;
    width: 22px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid rgba(60, 60, 67, 0.14);
    selection-background-color: rgba(10, 132, 255, 0.2);
}

QTableWidget,
QTableView {
    border: none;
    background: transparent;
    gridline-color: rgba(60, 60, 67, 0.08);
    selection-background-color: rgba(10, 132, 255, 0.2);
    alternate-background-color: rgba(245, 247, 252, 0.7);
}

QHeaderView::section {
    background-color: #f4f7fb;
    border: none;
    border-bottom: 1px solid rgba(60, 60, 67, 0.12);
    padding: 6px;
    font-weight: 600;
    color: #374151;
}

QScrollBar:vertical {
    width: 11px;
    background: transparent;
    margin: 2px;
}

QScrollBar::handle:vertical {
    border-radius: 5px;
    background: rgba(95, 105, 120, 0.45);
    min-height: 25px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    height: 0px;
    background: transparent;
}

QMessageBox {
    background-color: #f4f7fb;
}

QMessageBox QLabel {
    color: #111827;
    font-size: 13px;
    min-width: 420px;
}

QMessageBox QPushButton {
    min-width: 78px;
}
"""


MAC_DARK_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                stop: 0 #1a1f2a, stop: 1 #11151d);
}

QWidget {
    color: #e5e7eb;
    font-family: "SF Pro Text", "Helvetica Neue", "Segoe UI";
    font-size: 13px;
}

QFrame#Card {
    background-color: rgba(25, 30, 42, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
}

QFrame#ImageSurface {
    background-color: #151b28;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
}

QLabel#Title {
    font-size: 25px;
    font-weight: 700;
    color: #f3f4f6;
}

QLabel#Subtitle {
    font-size: 13px;
    color: #b0b7c5;
}

QLabel#FieldName {
    font-size: 12px;
    color: #9ca3af;
}

QLabel#FieldValue {
    font-size: 14px;
    font-weight: 600;
    color: #f3f4f6;
}

QLabel#Note {
    color: #a2aab9;
    font-size: 12px;
}

QFrame#TopControls {
    background-color: rgba(17, 23, 34, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
}

QPushButton {
    background-color: #0a84ff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2a93ff;
}

QPushButton:pressed {
    background-color: #0b6ed2;
}

QPushButton:disabled {
    background-color: #3a4355;
    color: #9da7b9;
}

QPushButton#SecondaryButton {
    background-color: #273041;
    color: #e5e7eb;
}

QPushButton#SecondaryButton:hover {
    background-color: #313c4f;
}

QPushButton#ToolbarButton {
    background-color: transparent;
    color: #d1d5db;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: 600;
}

QPushButton#ToolbarButton:hover {
    background-color: rgba(255, 255, 255, 0.08);
}

QPushButton#ToolbarButton:pressed {
    background-color: rgba(255, 255, 255, 0.14);
}

QPushButton#ToolbarButton:disabled {
    color: #7c879b;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background-color: transparent;
}

QPushButton#ToolbarIcon {
    background-color: transparent;
    color: #d1d5db;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    padding: 0px;
    font-weight: 700;
}

QPushButton#ToolbarIcon:hover {
    background-color: rgba(255, 255, 255, 0.08);
}

QPushButton#ToolbarIcon:pressed {
    background-color: rgba(255, 255, 255, 0.14);
}

QGraphicsView {
    border: none;
    background: transparent;
}

QSplitter::handle {
    background: transparent;
}

QSplitter::handle:horizontal {
    width: 12px;
    margin: 24px 2px;
    border-radius: 6px;
}

QSplitter::handle:horizontal:hover {
    background: rgba(255, 255, 255, 0.16);
}

QSplitter::handle:horizontal:pressed {
    background: rgba(10, 132, 255, 0.45);
}

QTabWidget::pane {
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    background-color: rgba(19, 25, 37, 0.92);
    top: -1px;
}

QTabBar::tab {
    background: #243042;
    color: #b9c2d3;
    padding: 7px 12px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background: #161d2a;
    color: #f3f4f6;
}

QComboBox {
    background-color: #273041;
    color: #e5e7eb;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 10px;
    padding: 6px 10px;
    min-width: 220px;
}

QComboBox:hover {
    background-color: #313c4f;
}

QComboBox::drop-down {
    border: none;
    width: 22px;
}

QComboBox QAbstractItemView {
    background-color: #131a29;
    border: 1px solid rgba(255, 255, 255, 0.14);
    selection-background-color: rgba(10, 132, 255, 0.35);
}

QTableWidget,
QTableView {
    border: none;
    background: transparent;
    gridline-color: rgba(255, 255, 255, 0.08);
    selection-background-color: rgba(10, 132, 255, 0.3);
    alternate-background-color: rgba(255, 255, 255, 0.03);
}

QHeaderView::section {
    background-color: #1f2938;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    padding: 6px;
    font-weight: 600;
    color: #d1d5db;
}

QScrollBar:vertical {
    width: 11px;
    background: transparent;
    margin: 2px;
}

QScrollBar::handle:vertical {
    border-radius: 5px;
    background: rgba(148, 163, 184, 0.45);
    min-height: 25px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    height: 0px;
    background: transparent;
}

QMessageBox {
    background-color: #1b2332;
}

QMessageBox QLabel {
    color: #f3f4f6;
    font-size: 13px;
    min-width: 420px;
}

QMessageBox QPushButton {
    min-width: 78px;
}
"""


def rgba_to_hex(r: int, g: int, b: int, a: int = 255) -> str:
    if a == 255:
        return f"#{r:02X}{g:02X}{b:02X}"
    return f"#{r:02X}{g:02X}{b:02X}{a:02X}"


def format_rgba(r: int, g: int, b: int, a: int = 255) -> str:
    return f"({r}, {g}, {b}, {a})"


def format_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def color_name(r: int, g: int, b: int, a: int = 255) -> str:
    if a == 0:
        return "Transparan"

    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    hue = h * 360

    if v <= 0.08:
        return "Hitam"
    if s <= 0.1:
        if v >= 0.93:
            return "Putih"
        if v >= 0.7:
            return "Abu-abu Terang"
        if v >= 0.35:
            return "Abu-abu"
        return "Abu-abu Gelap"

    if hue < 15 or hue >= 345:
        base = "Merah"
    elif hue < 45:
        base = "Oranye"
    elif hue < 70:
        base = "Kuning"
    elif hue < 165:
        base = "Hijau"
    elif hue < 200:
        base = "Cyan"
    elif hue < 255:
        base = "Biru"
    elif hue < 290:
        base = "Ungu"
    else:
        base = "Magenta"

    if v >= 0.85:
        return f"{base} Muda"
    if v <= 0.35:
        return f"{base} Tua"
    return base


class ExtractionWorker(QObject):
    finished = Signal(object, object, int, int)
    failed = Signal(str)
    progress = Signal(int, int)

    def __init__(self, pil_image: Image.Image, max_preview_pixels: int) -> None:
        super().__init__()
        self._image = pil_image
        self._max_preview_pixels = max_preview_pixels

    def run(self) -> None:
        try:
            width, height = self._image.size
            total_pixels = width * height

            counter: Counter[tuple[int, int, int, int]] = Counter()
            preview_rows: list[tuple[int, tuple[int, int, int, int]]] = []
            report_every = max(1, total_pixels // 40)

            pixel_stream = cast(
                Iterable[tuple[int, int, int, int]], self._image.getdata()
            )
            for index, rgba in enumerate(pixel_stream, start=1):
                counter[rgba] += 1
                if index <= self._max_preview_pixels:
                    preview_rows.append((index - 1, rgba))

                if index % report_every == 0 or index == total_pixels:
                    self.progress.emit(index, total_pixels)

            self.finished.emit(counter, preview_rows, width, total_pixels)
        except MemoryError:
            self.failed.emit(
                "Ekstraksi gagal karena penggunaan memori terlalu besar. Coba gambar dengan resolusi lebih kecil."
            )
        except Exception as exc:
            self.failed.emit(str(exc))


class ColorHighlightWorker(QObject):
    finished = Signal(object, int, object)
    failed = Signal(str)
    progress = Signal(int, int)

    def __init__(
        self,
        pil_image: Image.Image,
        target_rgba: tuple[int, int, int, int],
        overlay_rgba: tuple[int, int, int, int],
    ) -> None:
        super().__init__()
        self._image = pil_image
        self._target_rgba = target_rgba
        self._overlay_rgba = overlay_rgba

    def run(self) -> None:
        try:
            width, height = self._image.size
            total_pixels = width * height
            report_every = max(1, total_pixels // 40)

            r, g, b, a = self._overlay_rgba
            raw_overlay = bytearray(total_pixels * 4)
            matching_pixels = 0

            pixel_stream = cast(
                Iterable[tuple[int, int, int, int]], self._image.getdata()
            )
            for index, rgba in enumerate(pixel_stream):
                if rgba == self._target_rgba:
                    offset = index * 4
                    raw_overlay[offset] = r
                    raw_overlay[offset + 1] = g
                    raw_overlay[offset + 2] = b
                    raw_overlay[offset + 3] = a
                    matching_pixels += 1

                processed = index + 1
                if processed % report_every == 0 or processed == total_pixels:
                    self.progress.emit(processed, total_pixels)

            qimage = QImage(
                bytes(raw_overlay),
                width,
                height,
                width * 4,
                QImage.Format.Format_RGBA8888,
            ).copy()
            self.finished.emit(qimage, matching_pixels, self._target_rgba)
        except MemoryError:
            self.failed.emit(
                "Highlight warna gagal karena memori tidak cukup. Coba gambar dengan resolusi lebih kecil."
            )
        except Exception as exc:
            self.failed.emit(str(exc))


class PixelListModel(QAbstractTableModel):
    HEADERS = ("Warna", "X", "Y", "HEX", "RGBA", "Nama")

    def __init__(self) -> None:
        super().__init__()
        self._image: Image.Image | None = None
        self._pixel_stream = None
        self._width = 0
        self._height = 0
        self._total_pixels = 0
        self._last_row = -1
        self._last_rgba: tuple[int, int, int, int] = (0, 0, 0, 0)

    def set_image(self, image: Image.Image | None) -> None:
        self.beginResetModel()
        self._image = image
        if image is None:
            self._pixel_stream = None
            self._width = 0
            self._height = 0
            self._total_pixels = 0
        else:
            self._pixel_stream = image.getdata()
            self._width, self._height = image.size
            self._total_pixels = self._width * self._height
        self._last_row = -1
        self._last_rgba = (0, 0, 0, 0)
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return self._total_pixels

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.HEADERS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole,
    ) -> str | None:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and 0 <= section < len(self.HEADERS):
            return self.HEADERS[section]
        return None

    def _rgba_for_row(self, row: int) -> tuple[int, int, int, int]:
        if row == self._last_row:
            return self._last_rgba

        if self._image is None or self._width <= 0:
            return (0, 0, 0, 0)

        x = row % self._width
        y = row // self._width
        if self._pixel_stream is None:
            pixel = self._image.getpixel((x, y))
        else:
            try:
                pixel = self._pixel_stream[row]
            except Exception:
                pixel = self._image.getpixel((x, y))

        def _to_int(value: object) -> int:
            if isinstance(value, bool):
                return int(value)
            if isinstance(value, int):
                return value
            if isinstance(value, float):
                return int(value)
            return 0

        if isinstance(pixel, int):
            rgba = (pixel, pixel, pixel, 255)
        elif isinstance(pixel, tuple):
            if len(pixel) >= 4:
                rgba = (
                    _to_int(pixel[0]),
                    _to_int(pixel[1]),
                    _to_int(pixel[2]),
                    _to_int(pixel[3]),
                )
            elif len(pixel) == 3:
                rgba = (_to_int(pixel[0]), _to_int(pixel[1]), _to_int(pixel[2]), 255)
            else:
                value = _to_int(pixel[0]) if pixel else 0
                rgba = (value, value, value, 255)
        elif isinstance(pixel, list):
            if len(pixel) >= 4:
                rgba = (
                    _to_int(pixel[0]),
                    _to_int(pixel[1]),
                    _to_int(pixel[2]),
                    _to_int(pixel[3]),
                )
            elif len(pixel) == 3:
                rgba = (_to_int(pixel[0]), _to_int(pixel[1]), _to_int(pixel[2]), 255)
            else:
                value = _to_int(pixel[0]) if pixel else 0
                rgba = (value, value, value, 255)
        else:
            value = _to_int(pixel)
            rgba = (value, value, value, 255)

        self._last_row = row
        self._last_rgba = rgba
        return rgba

    def pixel_info(self, row: int) -> tuple[int, int, tuple[int, int, int, int]] | None:
        if (
            self._image is None
            or row < 0
            or row >= self._total_pixels
            or self._width <= 0
        ):
            return None
        x = row % self._width
        y = row // self._width
        return x, y, self._rgba_for_row(row)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> object:
        if not index.isValid() or self._image is None:
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= self._total_pixels or self._width <= 0:
            return None

        x = row % self._width
        y = row // self._width
        r, g, b, a = self._rgba_for_row(row)

        if role == Qt.DisplayRole:
            if col == 0:
                return ""
            if col == 1:
                return str(x)
            if col == 2:
                return str(y)
            if col == 3:
                return rgba_to_hex(r, g, b, a)
            if col == 4:
                return format_rgba(r, g, b, a)
            if col == 5:
                return color_name(r, g, b, a)

        if role == Qt.BackgroundRole and col == 0:
            return QBrush(QColor(r, g, b, a))

        if role == Qt.TextAlignmentRole and col in {1, 2}:
            return int(Qt.AlignCenter)

        if role == Qt.UserRole:
            return (x, y, (r, g, b, a))

        return None


class ColorImageView(QGraphicsView):
    pixelHovered = Signal(int, int, object)
    pixelClicked = Signal(int, int, object)
    hoverExited = Signal()
    zoomChanged = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)

        self._color_highlight_item = QGraphicsPixmapItem()
        self._scene.addItem(self._color_highlight_item)

        self._crosshair_horizontal = QGraphicsLineItem()
        self._crosshair_vertical = QGraphicsLineItem()
        self._pixel_outline = QGraphicsRectItem()
        self._selected_pixel_rect = QGraphicsRectItem()

        self._line_pen = QPen(QColor(255, 255, 255, 225))
        self._line_pen.setStyle(Qt.PenStyle.DashLine)
        self._line_pen.setWidth(1)
        self._line_pen.setCosmetic(True)

        self._outline_pen = QPen(QColor(10, 132, 255, 245))
        self._outline_pen.setWidth(2)
        self._outline_pen.setCosmetic(True)

        self._selected_pen = QPen(QColor(255, 189, 46, 240))
        self._selected_pen.setWidth(2)
        self._selected_pen.setCosmetic(True)
        self._selected_brush = QBrush(QColor(255, 189, 46, 64))

        self._crosshair_horizontal.setPen(self._line_pen)
        self._crosshair_vertical.setPen(self._line_pen)
        self._pixel_outline.setPen(self._outline_pen)
        self._selected_pixel_rect.setPen(self._selected_pen)
        self._selected_pixel_rect.setBrush(self._selected_brush)

        self._color_highlight_item.setZValue(12)
        self._crosshair_horizontal.setZValue(20)
        self._crosshair_vertical.setZValue(20)
        self._pixel_outline.setZValue(21)
        self._selected_pixel_rect.setZValue(22)

        self._scene.addItem(self._crosshair_horizontal)
        self._scene.addItem(self._crosshair_vertical)
        self._scene.addItem(self._pixel_outline)
        self._scene.addItem(self._selected_pixel_rect)

        self._qimage: QImage | None = None
        self._zoom_factor = 1.0
        self._zoom_step = 1.2
        self._zoom_min = 1.0
        self._zoom_max = 40.0
        self._auto_fit_on_resize = True

        self.setFrameShape(QFrame.NoFrame)
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setRenderHint(QPainter.SmoothPixmapTransform, False)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

        self._set_crosshair_visible(False)

    def load_image(self, qimage: QImage) -> None:
        self._qimage = qimage.convertToFormat(QImage.Format.Format_RGBA8888)
        self._pixmap_item.setPixmap(QPixmap.fromImage(self._qimage))
        self.setSceneRect(self._pixmap_item.boundingRect())
        self._set_crosshair_visible(False)
        self.clear_selected_pixel()
        self.clear_color_overlay()
        self._fit_to_view()

    def has_image(self) -> bool:
        return self._qimage is not None and not self._qimage.isNull()

    def _fit_to_view(self) -> None:
        if not self.has_image():
            return
        self.resetTransform()
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
        self._zoom_factor = 1.0
        self._auto_fit_on_resize = True
        self.zoomChanged.emit(self._zoom_factor)

    def zoom_in(self, centered: bool = True) -> None:
        self._zoom_to(self._zoom_factor * self._zoom_step, centered=centered)

    def zoom_out(self, centered: bool = True) -> None:
        self._zoom_to(self._zoom_factor / self._zoom_step, centered=centered)

    def reset_zoom(self) -> None:
        self._fit_to_view()

    def _zoom_to(self, target_zoom: float, centered: bool) -> None:
        if not self.has_image():
            return

        clamped_zoom = max(self._zoom_min, min(target_zoom, self._zoom_max))
        if abs(clamped_zoom - self._zoom_factor) < 1e-6:
            return

        current_anchor = self.transformationAnchor()
        if centered:
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        else:
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        step_factor = clamped_zoom / self._zoom_factor
        self.scale(step_factor, step_factor)

        self.setTransformationAnchor(current_anchor)
        self._zoom_factor = clamped_zoom
        self._auto_fit_on_resize = self._zoom_factor <= 1.0001
        self.zoomChanged.emit(self._zoom_factor)

    def focus_pixel(self, x: int, y: int) -> None:
        if not self.has_image() or self._qimage is None:
            return

        if x < 0 or y < 0 or x >= self._qimage.width() or y >= self._qimage.height():
            return

        self._update_crosshair(x, y)
        self.centerOn(x + 0.5, y + 0.5)

    def set_selected_pixel(self, x: int, y: int) -> None:
        if not self.has_image() or self._qimage is None:
            return
        if x < 0 or y < 0 or x >= self._qimage.width() or y >= self._qimage.height():
            self.clear_selected_pixel()
            return

        self._selected_pixel_rect.setRect(x, y, 1, 1)
        self._selected_pixel_rect.setVisible(True)

    def clear_selected_pixel(self) -> None:
        self._selected_pixel_rect.setVisible(False)

    def set_color_overlay(self, qimage: QImage | None) -> None:
        if qimage is None or qimage.isNull():
            self.clear_color_overlay()
            return

        self._color_highlight_item.setPixmap(QPixmap.fromImage(qimage))
        self._color_highlight_item.setVisible(True)

    def clear_color_overlay(self) -> None:
        self._color_highlight_item.setPixmap(QPixmap())
        self._color_highlight_item.setVisible(False)

    def _set_crosshair_visible(self, visible: bool) -> None:
        self._crosshair_horizontal.setVisible(visible)
        self._crosshair_vertical.setVisible(visible)
        self._pixel_outline.setVisible(visible)

    def _update_crosshair(self, x: int, y: int) -> None:
        if not self.has_image():
            self._set_crosshair_visible(False)
            return

        bounds = self._pixmap_item.boundingRect()
        center_x = x + 0.5
        center_y = y + 0.5

        self._crosshair_horizontal.setLine(
            bounds.left(),
            center_y,
            bounds.right(),
            center_y,
        )
        self._crosshair_vertical.setLine(
            center_x,
            bounds.top(),
            center_x,
            bounds.bottom(),
        )
        self._pixel_outline.setRect(x, y, 1, 1)
        self._set_crosshair_visible(True)

    def _map_to_pixel(
        self, view_pos
    ) -> tuple[int, int, tuple[int, int, int, int]] | None:
        if not self.has_image() or self._qimage is None:
            return None

        scene_pos = self.mapToScene(view_pos)
        x = int(scene_pos.x())
        y = int(scene_pos.y())

        if x < 0 or y < 0 or x >= self._qimage.width() or y >= self._qimage.height():
            return None

        qcolor = self._qimage.pixelColor(x, y)
        return x, y, (qcolor.red(), qcolor.green(), qcolor.blue(), qcolor.alpha())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pixel_info = self._map_to_pixel(event.position().toPoint())
        if pixel_info is None:
            self._set_crosshair_visible(False)
            self.hoverExited.emit()
        else:
            x, y, rgba = pixel_info
            self._update_crosshair(x, y)
            self.pixelHovered.emit(x, y, rgba)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            pixel_info = self._map_to_pixel(event.position().toPoint())
            if pixel_info is not None:
                x, y, rgba = pixel_info
                self._update_crosshair(x, y)
                self.pixelClicked.emit(x, y, rgba)
        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self.has_image():
            super().wheelEvent(event)
            return

        delta = event.angleDelta().y()
        if delta == 0:
            super().wheelEvent(event)
            return

        if delta > 0:
            self.zoom_in(centered=False)
        else:
            self.zoom_out(centered=False)
        event.accept()

    def leaveEvent(self, event) -> None:
        self._set_crosshair_visible(False)
        self.hoverExited.emit()
        super().leaveEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self._auto_fit_on_resize:
            self._fit_to_view()


class ThemeSwitch(QAbstractButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setFixedSize(44, 24)
        self._dark_surface = False
        self.toggled.connect(self.update)

    def sizeHint(self) -> QSize:
        return QSize(44, 24)

    def set_dark_surface(self, dark: bool) -> None:
        self._dark_surface = dark
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = QRectF(1, 1, self.width() - 2, self.height() - 2)
        radius = rect.height() / 2

        if self.isChecked():
            track_color = QColor(10, 132, 255)
            if self.underMouse():
                track_color = QColor(42, 147, 255)
        elif self._dark_surface:
            track_color = QColor(82, 94, 115)
            if self.underMouse():
                track_color = QColor(99, 112, 135)
        else:
            track_color = QColor(193, 201, 214)
            if self.underMouse():
                track_color = QColor(177, 187, 202)

        border_color = (
            QColor(255, 255, 255, 42) if self._dark_surface else QColor(60, 60, 67, 48)
        )

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(track_color)
        painter.drawRoundedRect(rect, radius, radius)

        knob_diameter = rect.height() - 6
        knob_y = rect.top() + 3
        knob_x = (
            rect.right() - 3 - knob_diameter if self.isChecked() else rect.left() + 3
        )

        knob_color = (
            QColor(243, 244, 246) if self._dark_surface else QColor(255, 255, 255)
        )
        painter.setPen(QPen(QColor(0, 0, 0, 22), 1))
        painter.setBrush(knob_color)
        painter.drawEllipse(QRectF(knob_x, knob_y, knob_diameter, knob_diameter))

    def enterEvent(self, event) -> None:
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.update()
        super().leaveEvent(event)


class MainWindow(QMainWindow):
    MAX_PREVIEW_PIXELS = 10000
    MAX_UNIQUE_ROWS = 4000
    IMAGE_FILTER = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tif *.tiff)"

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("ColorPoint - Pixel Color Extractor")
        self.resize(1320, 840)
        self.setAcceptDrops(True)

        self._settings = QSettings("ColorPoint", "ColorPoint")
        self._is_dark_theme = False

        self.pil_image: Image.Image | None = None
        self.image_path: Path | None = None
        self.unique_counter: Counter[tuple[int, int, int, int]] = Counter()
        self.all_pixels_model = PixelListModel()

        self._is_analyzing = False
        self._analysis_thread: QThread | None = None
        self._analysis_worker: ExtractionWorker | None = None

        self._is_highlighting = False
        self._highlight_thread: QThread | None = None
        self._highlight_worker: ColorHighlightWorker | None = None
        self._pending_highlight_color: tuple[int, int, int, int] | None = None
        self._current_overlay_color: tuple[int, int, int, int] | None = None
        self._selected_pixel: tuple[int, int, tuple[int, int, int, int]] | None = None
        self._shortcuts: list[QShortcut] = []
        self._inspector_rgba: tuple[int, int, int, int] = (229, 233, 241, 255)

        self._build_ui()
        self._setup_shortcuts()
        self._apply_tooltips()
        self._bind_events()
        self._is_dark_theme = self._read_theme_setting()
        self._apply_theme(self._is_dark_theme, persist=False)
        self._set_default_state()

    def _build_ui(self) -> None:
        container = QWidget()
        root = QVBoxLayout(container)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title = QLabel("ColorPoint")
        title.setObjectName("Title")
        subtitle = QLabel(
            "Ekstrak warna gambar hingga level pixel, lengkap dengan HEX dan nama warna."
        )
        subtitle.setObjectName("Subtitle")
        text_col.addWidget(title)
        text_col.addWidget(subtitle)
        top_row.addLayout(text_col)

        top_row.addStretch(1)

        controls_frame = QFrame()
        controls_frame.setObjectName("TopControls")
        controls_row = QHBoxLayout(controls_frame)
        controls_row.setContentsMargins(8, 6, 8, 6)
        controls_row.setSpacing(6)

        self.help_button = QPushButton("?")
        self.theme_toggle_button = ThemeSwitch()
        self.open_button = QPushButton("Upload")
        self.export_button = QPushButton("Ekspor CSV")
        self.zoom_out_button = QPushButton("-")
        self.zoom_in_button = QPushButton("+")
        self.zoom_reset_button = QPushButton("100%")

        self.help_button.setObjectName("ToolbarIcon")
        self.open_button.setObjectName("ToolbarButton")
        self.export_button.setObjectName("ToolbarButton")
        self.zoom_out_button.setObjectName("ToolbarButton")
        self.zoom_in_button.setObjectName("ToolbarButton")
        self.zoom_reset_button.setObjectName("ToolbarButton")

        self.help_button.setFixedSize(30, 30)
        self.open_button.setFixedHeight(30)
        self.export_button.setFixedHeight(30)
        self.zoom_out_button.setFixedSize(30, 30)
        self.zoom_in_button.setFixedSize(30, 30)
        self.zoom_reset_button.setFixedSize(54, 30)

        controls_row.addWidget(self.help_button)
        controls_row.addWidget(self.theme_toggle_button)
        controls_row.addSpacing(10)
        controls_row.addWidget(self.open_button)
        controls_row.addWidget(self.export_button)
        controls_row.addSpacing(2)
        controls_row.addWidget(self.zoom_out_button)
        controls_row.addWidget(self.zoom_in_button)
        controls_row.addWidget(self.zoom_reset_button)

        top_row.addWidget(controls_frame)
        root.addLayout(top_row)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(12)

        left_card = QFrame()
        left_card.setObjectName("Card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(14, 14, 14, 14)
        left_layout.setSpacing(8)

        guide = QLabel(
            "Arahkan cursor untuk baca warna pixel real-time. Gunakan scroll mouse untuk zoom, lalu klik untuk memilih pixel."
        )
        guide.setObjectName("Note")
        left_layout.addWidget(guide)

        image_surface = QFrame()
        image_surface.setObjectName("ImageSurface")
        image_layout = QVBoxLayout(image_surface)
        image_layout.setContentsMargins(10, 10, 10, 10)

        self.image_view = ColorImageView()
        self.image_view.setMinimumSize(640, 620)
        image_layout.addWidget(self.image_view)
        left_layout.addWidget(image_surface, 1)

        splitter.addWidget(left_card)

        right_card = QFrame()
        right_card.setObjectName("Card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(14, 14, 14, 14)
        right_layout.setSpacing(10)

        inspector_title = QLabel("Inspector Pixel")
        inspector_title.setObjectName("FieldValue")
        right_layout.addWidget(inspector_title)

        inspector_row = QHBoxLayout()
        inspector_row.setSpacing(12)

        self.main_swatch = QLabel()
        self.main_swatch.setFixedSize(86, 86)
        self._refresh_main_swatch_style()
        inspector_row.addWidget(self.main_swatch)

        fields = QVBoxLayout()
        fields.setSpacing(6)
        self.coord_value = self._make_info_field(fields, "Koordinat", "-")
        self.hex_value = self._make_info_field(fields, "HEX", "-")
        self.rgba_value = self._make_info_field(fields, "RGBA", "-")
        self.name_value = self._make_info_field(fields, "Nama Warna", "-")
        inspector_row.addLayout(fields, 1)

        right_layout.addLayout(inspector_row)

        self.tabs = QTabWidget()
        right_layout.addWidget(self.tabs, 1)

        unique_tab = QWidget()
        unique_layout = QVBoxLayout(unique_tab)
        unique_layout.setContentsMargins(10, 10, 10, 10)
        unique_layout.setSpacing(8)

        self.unique_info_label = QLabel("Belum ada data warna.")
        self.unique_info_label.setObjectName("Note")
        unique_layout.addWidget(self.unique_info_label)

        self.unique_table = QTableWidget(0, 6)
        self.unique_table.setHorizontalHeaderLabels(
            ["Warna", "Nama", "HEX", "RGBA", "Jumlah", "% Pixel"]
        )
        self._prepare_table(self.unique_table)
        self.unique_table.setAlternatingRowColors(True)
        unique_layout.addWidget(self.unique_table, 1)

        pixel_tab = QWidget()
        pixel_layout = QVBoxLayout(pixel_tab)
        pixel_layout.setContentsMargins(10, 10, 10, 10)
        pixel_layout.setSpacing(8)

        self.pixel_info_label = QLabel("Belum ada daftar pixel.")
        self.pixel_info_label.setObjectName("Note")
        pixel_layout.addWidget(self.pixel_info_label)

        self.pixel_table = QTableWidget(0, 6)
        self.pixel_table.setHorizontalHeaderLabels(
            ["Warna", "X", "Y", "Nama", "HEX", "RGBA"]
        )
        self._prepare_table(self.pixel_table)
        self.pixel_table.setAlternatingRowColors(True)
        pixel_layout.addWidget(self.pixel_table, 1)

        self.all_pixels_tab = QWidget()
        all_pixels_layout = QVBoxLayout(self.all_pixels_tab)
        all_pixels_layout.setContentsMargins(10, 10, 10, 10)
        all_pixels_layout.setSpacing(8)

        mode_row = QHBoxLayout()
        mode_row.setSpacing(8)
        mode_name = QLabel("Mode Highlight")
        mode_name.setObjectName("FieldName")

        self.highlight_mode_combo = QComboBox()
        self.highlight_mode_combo.addItem("Hanya Pixel Dipilih", "pixel")
        self.highlight_mode_combo.addItem("Semua Pixel Warna Sama", "color")

        self.clear_highlight_button = QPushButton("Hapus Highlight")
        self.clear_highlight_button.setObjectName("SecondaryButton")

        mode_row.addWidget(mode_name)
        mode_row.addWidget(self.highlight_mode_combo)
        mode_row.addWidget(self.clear_highlight_button)
        mode_row.addStretch(1)
        all_pixels_layout.addLayout(mode_row)

        self.all_pixels_info_label = QLabel("Belum ada data pixel.")
        self.all_pixels_info_label.setObjectName("Note")
        all_pixels_layout.addWidget(self.all_pixels_info_label)

        self.all_pixels_table = QTableView()
        self._prepare_all_pixels_table(self.all_pixels_table)
        self.all_pixels_table.setModel(self.all_pixels_model)
        all_pixels_layout.addWidget(self.all_pixels_table, 1)

        self.tabs.addTab(unique_tab, "Warna Unik")
        self.tabs.addTab(pixel_tab, "Preview Pixel")
        self.tabs.addTab(self.all_pixels_tab, "Semua Pixel")

        self.status_label = QLabel("Upload gambar untuk memulai.")
        self.status_label.setObjectName("Note")
        right_layout.addWidget(self.status_label)

        splitter.addWidget(right_card)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        root.addWidget(splitter, 1)
        self.setCentralWidget(container)

        self.setStyleSheet(MAC_STYLE)

    def _prepare_table(self, table: QTableWidget) -> None:
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(28)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def _prepare_all_pixels_table(self, table: QTableView) -> None:
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setAlternatingRowColors(True)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(28)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def _make_info_field(
        self, parent_layout: QVBoxLayout, title: str, default: str
    ) -> QLabel:
        name = QLabel(title)
        name.setObjectName("FieldName")
        value = QLabel(default)
        value.setObjectName("FieldValue")
        parent_layout.addWidget(name)
        parent_layout.addWidget(value)
        return value

    def _bind_events(self) -> None:
        self.help_button.clicked.connect(self._show_quick_help)
        self.theme_toggle_button.toggled.connect(self._on_theme_toggled)
        self.open_button.clicked.connect(self.open_image_dialog)
        self.export_button.clicked.connect(self.export_all_pixels)
        self.zoom_out_button.clicked.connect(self._zoom_out_image)
        self.zoom_in_button.clicked.connect(self._zoom_in_image)
        self.zoom_reset_button.clicked.connect(self._reset_image_zoom)

        self.image_view.pixelHovered.connect(self._on_pixel_hovered)
        self.image_view.pixelClicked.connect(self._on_pixel_clicked)
        self.image_view.hoverExited.connect(self._on_hover_exited)
        self.image_view.zoomChanged.connect(self._on_zoom_changed)

        self.unique_table.cellClicked.connect(self._on_unique_table_clicked)
        self.pixel_table.cellClicked.connect(self._on_pixel_table_clicked)
        self.all_pixels_table.clicked.connect(self._on_all_pixels_clicked)
        self.highlight_mode_combo.currentIndexChanged.connect(
            self._on_highlight_mode_changed
        )
        self.clear_highlight_button.clicked.connect(self._clear_highlight)

    def _setup_shortcuts(self) -> None:
        self._shortcuts = [
            QShortcut(QKeySequence("Ctrl+O"), self),
            QShortcut(QKeySequence("Ctrl+S"), self),
            QShortcut(QKeySequence("Ctrl+="), self),
            QShortcut(QKeySequence("Ctrl+-"), self),
            QShortcut(QKeySequence("Ctrl+0"), self),
            QShortcut(QKeySequence("Ctrl+L"), self),
            QShortcut(QKeySequence("F1"), self),
            QShortcut(QKeySequence("Ctrl+D"), self),
        ]
        self._shortcuts[0].activated.connect(self.open_image_dialog)
        self._shortcuts[1].activated.connect(self.export_all_pixels)
        self._shortcuts[2].activated.connect(self._zoom_in_image)
        self._shortcuts[3].activated.connect(self._zoom_out_image)
        self._shortcuts[4].activated.connect(self._reset_image_zoom)
        self._shortcuts[5].activated.connect(self._clear_highlight)
        self._shortcuts[6].activated.connect(self._show_quick_help)
        self._shortcuts[7].activated.connect(lambda: self.theme_toggle_button.toggle())

    def _apply_tooltips(self) -> None:
        self.help_button.setToolTip("Buka panduan cepat penggunaan (F1)")
        self.theme_toggle_button.setToolTip("Aktif/nonaktifkan dark mode (Ctrl+D)")
        self.open_button.setToolTip("Upload gambar baru (Ctrl+O)")
        self.export_button.setToolTip("Ekspor semua pixel ke CSV (Ctrl+S)")
        self.zoom_in_button.setToolTip("Perbesar gambar (Ctrl+=)")
        self.zoom_out_button.setToolTip("Perkecil gambar (Ctrl+-)")
        self.zoom_reset_button.setToolTip("Reset zoom ke ukuran fit (Ctrl+0)")
        self.highlight_mode_combo.setToolTip(
            "Pilih mode highlight untuk pixel yang dipilih"
        )
        self.clear_highlight_button.setToolTip("Hapus highlight aktif (Ctrl+L)")
        self.all_pixels_table.setToolTip(
            "Klik row pixel untuk sinkron ke preview dan inspector"
        )

    def _read_theme_setting(self) -> bool:
        saved_value = self._settings.value("ui/dark_mode", False)
        if isinstance(saved_value, bool):
            return saved_value
        if isinstance(saved_value, str):
            return saved_value.strip().lower() in {"1", "true", "yes", "on"}
        if isinstance(saved_value, int):
            return saved_value != 0
        return False

    def _swatch_border_color(self) -> str:
        if self._is_dark_theme:
            return "rgba(255,255,255,0.24)"
        return "rgba(60,60,67,0.24)"

    def _refresh_main_swatch_style(self) -> None:
        r, g, b, a = self._inspector_rgba
        self.main_swatch.setStyleSheet(
            f"background-color: rgba({r}, {g}, {b}, {a});"
            f"border: 1px solid {self._swatch_border_color()};"
            "border-radius: 16px;"
        )

    def _apply_theme(self, dark_mode: bool, persist: bool = True) -> None:
        self._is_dark_theme = dark_mode
        self.setStyleSheet(MAC_DARK_STYLE if dark_mode else MAC_STYLE)

        self.theme_toggle_button.blockSignals(True)
        self.theme_toggle_button.setChecked(dark_mode)
        self.theme_toggle_button.set_dark_surface(dark_mode)
        self.theme_toggle_button.blockSignals(False)

        self._refresh_main_swatch_style()

        if persist:
            self._settings.setValue("ui/dark_mode", dark_mode)

    def _on_theme_toggled(self, checked: bool) -> None:
        self._apply_theme(checked)

    def _show_quick_help(self) -> None:
        QMessageBox.information(
            self,
            "Panduan Cepat",
            "1) Upload gambar lalu arahkan cursor ke preview untuk baca warna real-time.\n"
            "2) Klik gambar atau row tabel untuk memilih pixel.\n"
            "3) Tab 'Semua Pixel' punya 2 mode: pixel saja / semua warna sama.\n"
            "4) Pakai switch Dark untuk ganti tema terang/gelap.\n"
            "5) Shortcut: Ctrl+O upload, Ctrl+S export, Ctrl+= zoom in, Ctrl+- zoom out, Ctrl+0 reset, Ctrl+L clear highlight, Ctrl+D dark mode.",
        )

    def _set_default_state(self) -> None:
        self.export_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)
        self.zoom_in_button.setEnabled(False)
        self.zoom_reset_button.setEnabled(False)
        self.highlight_mode_combo.setEnabled(False)
        self.clear_highlight_button.setEnabled(False)

    def _zoom_out_image(self) -> None:
        self.image_view.zoom_out(centered=True)

    def _zoom_in_image(self) -> None:
        self.image_view.zoom_in(centered=True)

    def _reset_image_zoom(self) -> None:
        self.image_view.reset_zoom()

    def _on_zoom_changed(self, zoom_factor: float) -> None:
        self.zoom_reset_button.setText(f"{zoom_factor * 100:.0f}%")

    def open_image_dialog(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih gambar",
            "",
            self.IMAGE_FILTER,
        )
        if not file_path:
            return
        self.load_image(Path(file_path))

    def load_image(self, path: Path) -> None:
        qimage = QImage(str(path))
        if qimage.isNull():
            QMessageBox.warning(self, "Gagal", "Gambar tidak bisa dibuka.")
            return

        try:
            with Image.open(path) as opened_image:
                self.pil_image = opened_image.convert("RGBA").copy()
        except OSError as exc:
            QMessageBox.warning(self, "Gagal", f"Tidak bisa membaca gambar: {exc}")
            return

        self.image_path = path
        self.image_view.load_image(qimage)
        self.export_button.setEnabled(True)
        self.zoom_out_button.setEnabled(True)
        self.zoom_in_button.setEnabled(True)
        self.zoom_reset_button.setEnabled(True)
        self.highlight_mode_combo.setEnabled(True)

        self._selected_pixel = None
        self._pending_highlight_color = None
        self._current_overlay_color = None
        self.image_view.clear_selected_pixel()
        self.image_view.clear_color_overlay()
        self.clear_highlight_button.setEnabled(False)

        self.all_pixels_model.set_image(self.pil_image)
        self.all_pixels_table.clearSelection()

        width, height = self.pil_image.size
        total_pixels = width * height
        self.all_pixels_info_label.setText(
            f"Total {format_number(total_pixels)} pixel. Pilih baris untuk highlight di image preview."
        )
        self.status_label.setText(f"Gambar aktif: {path.name} ({width}x{height})")
        self.analyze_colors()

    def analyze_colors(self) -> None:
        if self.pil_image is None:
            QMessageBox.information(
                self, "Info", "Silakan upload gambar terlebih dahulu."
            )
            return

        if self._is_analyzing:
            return

        image_for_analysis = self.pil_image.copy()
        self._set_busy_state(True)
        self.status_label.setText("Sedang mengekstrak warna... 0%")

        thread = QThread(self)
        worker = ExtractionWorker(image_for_analysis, self.MAX_PREVIEW_PIXELS)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.progress.connect(self._on_analysis_progress)
        worker.finished.connect(self._on_analysis_finished)
        worker.failed.connect(self._on_analysis_failed)

        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._cleanup_analysis_worker)

        self._analysis_thread = thread
        self._analysis_worker = worker
        thread.start()

    def _set_busy_state(self, busy: bool) -> None:
        self._is_analyzing = busy
        has_image = self.pil_image is not None
        allow_io = (not busy) and (not self._is_highlighting)
        self.open_button.setEnabled(allow_io)
        self.export_button.setEnabled(allow_io and has_image)
        self.highlight_mode_combo.setEnabled((not busy) and has_image)
        self.clear_highlight_button.setEnabled(
            (not busy) and has_image and self._selected_pixel is not None
        )

    def _set_highlight_busy(self, busy: bool) -> None:
        self._is_highlighting = busy
        has_image = self.pil_image is not None
        allow_io = (not self._is_analyzing) and (not busy)
        self.open_button.setEnabled(allow_io)
        self.export_button.setEnabled(allow_io and has_image)
        self.highlight_mode_combo.setEnabled((not self._is_analyzing) and has_image)
        self.clear_highlight_button.setEnabled(
            (not self._is_analyzing) and has_image and self._selected_pixel is not None
        )

    def _current_highlight_mode(self) -> str:
        mode_data = self.highlight_mode_combo.currentData()
        if mode_data in {"pixel", "color"}:
            return mode_data
        return "pixel"

    def _apply_selection_highlight(
        self,
        x: int,
        y: int,
        rgba: tuple[int, int, int, int],
    ) -> None:
        self._selected_pixel = (x, y, rgba)
        self.clear_highlight_button.setEnabled(True)
        self.image_view.set_selected_pixel(x, y)
        self.image_view.focus_pixel(x, y)

        if self._is_analyzing:
            self._pending_highlight_color = None
            self._current_overlay_color = None
            self.image_view.clear_color_overlay()
            self.all_pixels_info_label.setText(
                "Tunggu ekstraksi selesai untuk menggunakan highlight warna penuh."
            )
            return

        mode = self._current_highlight_mode()
        if mode == "pixel":
            self._pending_highlight_color = None
            self._current_overlay_color = None
            self.image_view.clear_color_overlay()
            self.all_pixels_info_label.setText(
                f"Highlight mode: Pixel. Titik ({x}, {y}) dipilih."
            )
            return

        self._request_color_highlight(rgba)

    def _sync_all_pixels_selection(self, x: int, y: int) -> None:
        if self.pil_image is None:
            return

        width, height = self.pil_image.size
        if width <= 0 or height <= 0:
            return
        if x < 0 or y < 0 or x >= width or y >= height:
            return

        row = (y * width) + x
        if row < 0 or row >= self.all_pixels_model.rowCount():
            return

        self.all_pixels_table.selectRow(row)
        index = self.all_pixels_model.index(row, 0)
        if index.isValid():
            self.all_pixels_table.setCurrentIndex(index)
            self.all_pixels_table.scrollTo(index, QAbstractItemView.PositionAtCenter)

    def _open_all_pixels_tab(self) -> None:
        tab_index = self.tabs.indexOf(self.all_pixels_tab)
        if tab_index >= 0 and self.tabs.currentIndex() != tab_index:
            self.tabs.setCurrentIndex(tab_index)

    def _request_color_highlight(self, rgba: tuple[int, int, int, int]) -> None:
        if self.pil_image is None:
            return

        if self._current_overlay_color == rgba and not self._is_highlighting:
            return

        if self._is_highlighting:
            self._pending_highlight_color = rgba
            return

        self._set_highlight_busy(True)
        self._current_overlay_color = None
        self.image_view.clear_color_overlay()
        self.all_pixels_info_label.setText("Membuat highlight warna... 0%")

        thread = QThread(self)
        worker = ColorHighlightWorker(
            self.pil_image.copy(),
            rgba,
            (255, 189, 46, 120),
        )
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.progress.connect(self._on_color_highlight_progress)
        worker.finished.connect(self._on_color_highlight_finished)
        worker.failed.connect(self._on_color_highlight_failed)

        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._cleanup_color_highlight_worker)

        self._highlight_thread = thread
        self._highlight_worker = worker
        thread.start()

    def _on_color_highlight_progress(
        self,
        processed_pixels: int,
        total_pixels: int,
    ) -> None:
        if total_pixels <= 0:
            return
        if self._current_highlight_mode() != "color" or self._selected_pixel is None:
            return
        percent = int((processed_pixels / total_pixels) * 100)
        self.all_pixels_info_label.setText(f"Membuat highlight warna... {percent}%")

    def _on_color_highlight_finished(
        self,
        overlay: QImage,
        matching_pixels: int,
        target_rgba: tuple[int, int, int, int],
    ) -> None:
        self._set_highlight_busy(False)

        if (
            self._current_highlight_mode() == "color"
            and self._selected_pixel is not None
            and self._selected_pixel[2] == target_rgba
        ):
            self.image_view.set_color_overlay(overlay)
            self._current_overlay_color = target_rgba
            self.all_pixels_info_label.setText(
                f"Highlight aktif: {format_number(matching_pixels)} pixel dengan warna {rgba_to_hex(*target_rgba)}"
            )
        elif self._selected_pixel is not None:
            selected_x, selected_y, _ = self._selected_pixel
            self.all_pixels_info_label.setText(
                f"Highlight mode: Pixel. Titik ({selected_x}, {selected_y}) dipilih."
            )
        elif self.pil_image is not None:
            width, height = self.pil_image.size
            total_pixels = width * height
            self.all_pixels_info_label.setText(
                f"Total {format_number(total_pixels)} pixel. Pilih baris untuk highlight di image preview."
            )

        pending = self._pending_highlight_color
        self._pending_highlight_color = None
        if (
            pending is not None
            and self._current_highlight_mode() == "color"
            and self._selected_pixel is not None
            and self._selected_pixel[2] == pending
        ):
            self._request_color_highlight(pending)

    def _on_color_highlight_failed(self, message: str) -> None:
        self._set_highlight_busy(False)
        self._pending_highlight_color = None
        self._current_overlay_color = None
        QMessageBox.warning(
            self,
            "Highlight Gagal",
            f"Tidak bisa membuat highlight warna: {message}",
        )
        self.all_pixels_info_label.setText("Highlight warna gagal.")

    def _cleanup_color_highlight_worker(self) -> None:
        finished_thread = self.sender()
        if finished_thread is self._highlight_thread:
            self._highlight_worker = None
            self._highlight_thread = None

    def _on_highlight_mode_changed(self, _index: int) -> None:
        if self._selected_pixel is None:
            return

        x, y, rgba = self._selected_pixel
        if self._current_highlight_mode() == "pixel":
            self._pending_highlight_color = None
            self._current_overlay_color = None
            self.image_view.clear_color_overlay()
            self.all_pixels_info_label.setText(
                f"Highlight mode: Pixel. Titik ({x}, {y}) dipilih."
            )
            return

        self._request_color_highlight(rgba)

    def _clear_highlight(self) -> None:
        self._pending_highlight_color = None
        self._selected_pixel = None
        self._current_overlay_color = None
        self.image_view.clear_selected_pixel()
        self.image_view.clear_color_overlay()
        self.all_pixels_table.clearSelection()
        self.clear_highlight_button.setEnabled(False)

        if self.pil_image is not None:
            width, height = self.pil_image.size
            total_pixels = width * height
            self.all_pixels_info_label.setText(
                f"Total {format_number(total_pixels)} pixel. Pilih baris untuk highlight di image preview."
            )

    def _on_analysis_progress(self, processed_pixels: int, total_pixels: int) -> None:
        if total_pixels <= 0:
            return
        percent = int((processed_pixels / total_pixels) * 100)
        self.status_label.setText(f"Sedang mengekstrak warna... {percent}%")

    def _on_analysis_finished(
        self,
        counter: Counter[tuple[int, int, int, int]],
        preview_rows: list[tuple[int, tuple[int, int, int, int]]],
        width: int,
        total_pixels: int,
    ) -> None:
        self.unique_counter = counter
        self._populate_unique_table(counter, total_pixels)
        self._populate_pixel_preview(preview_rows, width, total_pixels)

        unique_count = len(counter)
        self.status_label.setText(
            f"Selesai ekstrak: {format_number(total_pixels)} pixel, {format_number(unique_count)} warna unik."
        )
        self._set_busy_state(False)

    def _on_analysis_failed(self, message: str) -> None:
        QMessageBox.critical(
            self, "Ekstraksi Gagal", f"Terjadi error saat ekstraksi warna: {message}"
        )
        self.status_label.setText("Ekstraksi gagal.")
        self._set_busy_state(False)

    def _cleanup_analysis_worker(self) -> None:
        finished_thread = self.sender()
        if finished_thread is self._analysis_thread:
            self._analysis_worker = None
            self._analysis_thread = None

    def _populate_unique_table(
        self,
        counter: Counter[tuple[int, int, int, int]],
        total_pixels: int,
    ) -> None:
        all_unique = len(counter)
        color_rows = counter.most_common(self.MAX_UNIQUE_ROWS)

        self.unique_table.setUpdatesEnabled(False)
        try:
            self.unique_table.setRowCount(len(color_rows))
            for row, (rgba, count) in enumerate(color_rows):
                r, g, b, a = rgba
                hex_code = rgba_to_hex(r, g, b, a)
                name = color_name(r, g, b, a)
                percent = (count / total_pixels) * 100 if total_pixels else 0

                swatch_item = QTableWidgetItem()
                swatch_item.setBackground(QColor(r, g, b, a))
                swatch_item.setData(Qt.UserRole, rgba)
                swatch_item.setData(Qt.UserRole + 1, (-1, -1))

                self.unique_table.setItem(row, 0, swatch_item)
                self.unique_table.setItem(row, 1, QTableWidgetItem(name))
                self.unique_table.setItem(row, 2, QTableWidgetItem(hex_code))
                self.unique_table.setItem(
                    row, 3, QTableWidgetItem(format_rgba(r, g, b, a))
                )
                self.unique_table.setItem(
                    row, 4, QTableWidgetItem(format_number(count))
                )
                self.unique_table.setItem(row, 5, QTableWidgetItem(f"{percent:.2f}%"))
        finally:
            self.unique_table.setUpdatesEnabled(True)

        if all_unique > self.MAX_UNIQUE_ROWS:
            self.unique_info_label.setText(
                f"Menampilkan {format_number(self.MAX_UNIQUE_ROWS)} dari {format_number(all_unique)} warna unik."
            )
        else:
            self.unique_info_label.setText(
                f"Total warna unik: {format_number(all_unique)}."
            )

    def _populate_pixel_preview(
        self,
        preview_rows: list[tuple[int, tuple[int, int, int, int]]],
        width: int,
        total_pixels: int,
    ) -> None:
        self.pixel_table.setUpdatesEnabled(False)
        try:
            self.pixel_table.setRowCount(len(preview_rows))

            for row, (index, rgba) in enumerate(preview_rows):
                x = index % width
                y = index // width
                r, g, b, a = rgba

                swatch_item = QTableWidgetItem()
                swatch_item.setBackground(QColor(r, g, b, a))
                swatch_item.setData(Qt.UserRole, rgba)
                swatch_item.setData(Qt.UserRole + 1, (x, y))

                self.pixel_table.setItem(row, 0, swatch_item)
                self.pixel_table.setItem(row, 1, QTableWidgetItem(str(x)))
                self.pixel_table.setItem(row, 2, QTableWidgetItem(str(y)))
                self.pixel_table.setItem(
                    row, 3, QTableWidgetItem(color_name(r, g, b, a))
                )
                self.pixel_table.setItem(
                    row, 4, QTableWidgetItem(rgba_to_hex(r, g, b, a))
                )
                self.pixel_table.setItem(
                    row, 5, QTableWidgetItem(format_rgba(r, g, b, a))
                )
        finally:
            self.pixel_table.setUpdatesEnabled(True)

        shown = len(preview_rows)
        if total_pixels > shown:
            self.pixel_info_label.setText(
                f"Menampilkan {format_number(shown)} pixel pertama dari {format_number(total_pixels)} pixel."
            )
        else:
            self.pixel_info_label.setText(
                f"Semua {format_number(total_pixels)} pixel ditampilkan."
            )

    def _update_inspector(
        self,
        x: int | None,
        y: int | None,
        rgba: tuple[int, int, int, int],
    ) -> None:
        r, g, b, a = rgba
        self.coord_value.setText("-" if x is None or y is None else f"{x}, {y}")
        self.hex_value.setText(rgba_to_hex(r, g, b, a))
        self.rgba_value.setText(format_rgba(r, g, b, a))
        self.name_value.setText(color_name(r, g, b, a))
        self._inspector_rgba = rgba
        self._refresh_main_swatch_style()

    def _on_pixel_hovered(
        self, x: int, y: int, rgba: tuple[int, int, int, int]
    ) -> None:
        self._update_inspector(x, y, rgba)

    def _on_pixel_clicked(
        self, x: int, y: int, rgba: tuple[int, int, int, int]
    ) -> None:
        self._update_inspector(x, y, rgba)
        self._apply_selection_highlight(x, y, rgba)
        self._sync_all_pixels_selection(x, y)
        self._open_all_pixels_tab()
        self.status_label.setText(
            f"Pixel dipilih di ({x}, {y}) -> {rgba_to_hex(*rgba)} | {color_name(*rgba)}"
        )

    def _on_hover_exited(self) -> None:
        self.coord_value.setText("-")

    def _on_unique_table_clicked(self, row: int, _column: int) -> None:
        swatch_item = self.unique_table.item(row, 0)
        if swatch_item is None:
            return
        rgba = swatch_item.data(Qt.UserRole)
        if rgba is None:
            return
        self._update_inspector(None, None, tuple(rgba))

    def _on_pixel_table_clicked(self, row: int, _column: int) -> None:
        swatch_item = self.pixel_table.item(row, 0)
        if swatch_item is None:
            return

        rgba = swatch_item.data(Qt.UserRole)
        coord = swatch_item.data(Qt.UserRole + 1)
        if rgba is None:
            return

        x, y = (None, None)
        if coord:
            x, y = coord
        self._update_inspector(x, y, tuple(rgba))
        if x is not None and y is not None:
            self._apply_selection_highlight(x, y, tuple(rgba))
            self._sync_all_pixels_selection(x, y)

    def _on_all_pixels_clicked(self, index: QModelIndex) -> None:
        pixel_info = self.all_pixels_model.pixel_info(index.row())
        if pixel_info is None:
            return

        x, y, rgba = pixel_info
        self._update_inspector(x, y, rgba)
        self._apply_selection_highlight(x, y, rgba)
        self.status_label.setText(
            f"Pixel dipilih di ({x}, {y}) -> {rgba_to_hex(*rgba)} | {color_name(*rgba)}"
        )

    def closeEvent(self, event) -> None:
        if self._is_analyzing or self._is_highlighting:
            QMessageBox.information(
                self,
                "Proses Sedang Berjalan",
                "Tunggu proses berjalan selesai dulu sebelum menutup aplikasi.",
            )
            event.ignore()
            return
        super().closeEvent(event)

    def export_all_pixels(self) -> None:
        if self.pil_image is None:
            QMessageBox.information(
                self, "Info", "Silakan upload gambar terlebih dahulu."
            )
            return

        suggested_name = "pixel_colors.csv"
        if self.image_path is not None:
            suggested_name = f"{self.image_path.stem}_pixel_colors.csv"

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan data pixel",
            suggested_name,
            "CSV (*.csv)",
        )
        if not output_path:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            width, _height = self.pil_image.size
            with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["x", "y", "hex", "nama_warna", "r", "g", "b", "a"])

                pixel_stream = cast(
                    Iterable[tuple[int, int, int, int]], self.pil_image.getdata()
                )
                for index, rgba in enumerate(pixel_stream):
                    x = index % width
                    y = index // width
                    r, g, b, a = rgba
                    writer.writerow(
                        [
                            x,
                            y,
                            rgba_to_hex(r, g, b, a),
                            color_name(r, g, b, a),
                            r,
                            g,
                            b,
                            a,
                        ]
                    )

            self.status_label.setText(f"Data pixel berhasil diekspor ke: {output_path}")
            QMessageBox.information(self, "Sukses", "Ekspor CSV selesai.")
        except OSError as exc:
            QMessageBox.critical(self, "Error", f"Gagal menulis file CSV: {exc}")
        finally:
            QApplication.restoreOverrideCursor()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self._is_analyzing or self._is_highlighting:
            event.ignore()
            return

        if not event.mimeData().hasUrls():
            event.ignore()
            return

        for url in event.mimeData().urls():
            if url.isLocalFile():
                suffix = Path(url.toLocalFile()).suffix.lower()
                if suffix in {
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".bmp",
                    ".gif",
                    ".webp",
                    ".tif",
                    ".tiff",
                }:
                    event.acceptProposedAction()
                    return

        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if self._is_analyzing or self._is_highlighting:
            event.ignore()
            return

        for url in event.mimeData().urls():
            if url.isLocalFile():
                file_path = Path(url.toLocalFile())
                if file_path.suffix.lower() in {
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".bmp",
                    ".gif",
                    ".webp",
                    ".tif",
                    ".tiff",
                }:
                    self.load_image(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()


def main() -> int:
    def _handle_unexpected_exception(exc_type, exc_value, exc_traceback) -> None:
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        QMessageBox.critical(
            None,
            "Error Tidak Terduga",
            f"Aplikasi mengalami error: {exc_value}",
        )

    sys.excepthook = _handle_unexpected_exception

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
