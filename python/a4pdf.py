# Copyright 2023 Jussi Pakkanen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import ctypes
import os
import math
from enum import Enum

class LineCapStyle(Enum):
    Butt = 0
    Round = 1
    Projection_Square = 2

class LineJoinStyle(Enum):
    Miter = 0
    Round = 1
    Bevel = 2

class Colorspace(Enum):
    DeviceRGB = 0
    DeviceGray = 1
    DeviceCMYK = 2

class A4PDFException(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

ec_type = ctypes.c_int32
enum_type = ctypes.c_int32

class FontId(ctypes.Structure):
    _fields_ = [('id', ctypes.c_int32)]

class ImageId(ctypes.Structure):
    _fields_ = [('id', ctypes.c_int32)]

cfunc_types = (

('a4pdf_options_new', [ctypes.c_void_p]),
('a4pdf_options_destroy', [ctypes.c_void_p]),
('a4pdf_options_set_colorspace', [ctypes.c_void_p, enum_type]),
('a4pdf_options_set_title', [ctypes.c_void_p, ctypes.c_char_p]),
('a4pdf_options_set_mediabox',
    [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]),

('a4pdf_generator_new', [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p]),
('a4pdf_generator_add_page', [ctypes.c_void_p, ctypes.c_void_p]),
('a4pdf_generator_embed_jpg', [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]),
('a4pdf_generator_load_font', [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]),
('a4pdf_generator_write', [ctypes.c_void_p]),
('a4pdf_generator_destroy', [ctypes.c_void_p]),
('a4pdf_page_draw_context_new', [ctypes.c_void_p, ctypes.c_void_p]),

('a4pdf_dc_cmd_B', [ctypes.c_void_p]),
('a4pdf_dc_cmd_Bstar', [ctypes.c_void_p]),
('a4pdf_dc_cmd_c', [ctypes.c_void_p,
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_cm', [ctypes.c_void_p,
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_f', [ctypes.c_void_p]),
('a4pdf_dc_cmd_h', [ctypes.c_void_p]),
('a4pdf_dc_cmd_J', [ctypes.c_void_p, enum_type]),
('a4pdf_dc_cmd_j', [ctypes.c_void_p, enum_type]),
('a4pdf_dc_cmd_k', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_l', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_m', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_q', [ctypes.c_void_p]),
('a4pdf_dc_cmd_Q', [ctypes.c_void_p]),
('a4pdf_dc_cmd_RG', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_rg', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_re', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_cmd_S', [ctypes.c_void_p]),
('a4pdf_dc_cmd_w', [ctypes.c_void_p, ctypes.c_double]),
('a4pdf_dc_draw_image',
    [ctypes.c_void_p, ImageId]),
('a4pdf_dc_render_utf8_text',
    [ctypes.c_void_p, ctypes.c_char_p, FontId, ctypes.c_double, ctypes.c_double, ctypes.c_double]),
('a4pdf_dc_render_text_obj',
    [ctypes.c_void_p, ctypes.c_void_p]),
('a4pdf_dc_destroy', [ctypes.c_void_p]),

('a4pdf_text_new', [ctypes.c_void_p]),
('a4pdf_text_destroy', [ctypes.c_void_p]),
('a4pdf_text_new', [ctypes.c_void_p]),
('a4pdf_text_cmd_Tc', [ctypes.c_void_p, ctypes.c_double]),
('a4pdf_text_cmd_Td', [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]),
('a4pdf_text_cmd_Tf', [ctypes.c_void_p, FontId, ctypes.c_double]),
)

libfile_name = 'liba4pdf.so'
if 'A4PDF_SO_OVERRIDE' in os.environ:
    libfile_name = os.environ['A4PDF_SO_OVERRIDE'] + '/' + libfile_name
libfile = ctypes.cdll.LoadLibrary(libfile_name)

for funcname, argtypes in cfunc_types:
    funcobj = getattr(libfile, funcname)
    if argtypes is not None:
        funcobj.argtypes = argtypes
    funcobj.restype = ec_type

# This is the only function in the public API not to return an errorcode.
libfile.a4pdf_error_message.argtypes = [ctypes.c_int32]
libfile.a4pdf_error_message.restype = ctypes.c_char_p

def get_error_message(errorcode):
    return libfile.a4pdf_error_message(errorcode).decode('UTF-8', errors='ignore')

def raise_with_error(errorcode):
    raise A4PDFException(get_error_message(errorcode))

def check_error(errorcode):
    if errorcode != 0:
        raise_with_error(errorcode)

def to_bytepath(filename):
    if isinstance(filename, bytes):
        return filename
    elif isinstance(filename, str):
        return filename.encode('UTF-8')
    else:
        return str(filename).encode('UTF-8')

class Options:
    def __init__(self):
        opt = ctypes.c_void_p()
        check_error(libfile.a4pdf_options_new(ctypes.pointer(opt)))
        self._as_parameter_ = opt

    def __del__(self):
        check_error(libfile.a4pdf_options_destroy(self))

    def set_colorspace(self, cs):
        if not isinstance(cs, Colorspace):
            raise A4PDFException('Argument not a colorspace object.')
        check_error(libfile.a4pdf_options_set_colorspace(self, cs.value))

    def set_title(self, title):
        if not isinstance(title, str):
            raise A4PDFException('Title must be an Unicode string.')
        bytes = title.encode('UTF-8')
        check_error(libfile.a4pdf_options_set_title(self, bytes))

    def set_mediabox(self, x, y, w, h):
        check_error(libfile.a4pdf_options_set_mediabox(self, x, y, w, h))

class DrawContext:
    def __init__(self, generator):
        dcptr = ctypes.c_void_p()
        check_error(libfile.a4pdf_page_draw_context_new(generator, ctypes.pointer(dcptr)))
        self._as_parameter_ = dcptr
        self.generator = generator

    def __del__(self):
        check_error(libfile.a4pdf_dc_destroy(self))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            self.generator.add_page(self)
        finally:
            self.generator = None # Not very elegant.

    def push_gstate(self):
        return StateContextManager(self)

    def cmd_B(self):
        check_error(libfile.a4pdf_dc_cmd_B(self))

    def cmd_Bstar(self):
        check_error(libfile.a4pdf_dc_cmd_Bstar(self))

    def cmd_c(self, x1, y1, x2, y2, x3, y3):
        check_error(libfile.a4pdf_dc_cmd_c(self, x1, y1, x2, y2, x3, y3))

    def cmd_cm(self, m1, m2, m3, m4, m5, m6):
        check_error(libfile.a4pdf_dc_cmd_cm(self, m1, m2, m3, m4, m5, m6))

    def cmd_f(self):
        check_error(libfile.a4pdf_dc_cmd_f(self))

    def cmd_h(self):
        check_error(libfile.a4pdf_dc_cmd_h(self))

    def cmd_J(self, cap_style):
        check_error(libfile.a4pdf_dc_cmd_J(self, cap_style.value))

    def cmd_j(self, join_style):
        check_error(libfile.a4pdf_dc_cmd_j(self, join_style.value))

    def cmd_k(self, c, m, y, k):
        check_error(libfile.a4pdf_dc_cmd_k(self, c, m, y, k))

    def cmd_l(self, x, y):
        check_error(libfile.a4pdf_dc_cmd_l(self, x, y))

    def cmd_q(self):
        check_error(libfile.a4pdf_dc_cmd_q(self))

    def cmd_Q(self):
        check_error(libfile.a4pdf_dc_cmd_Q(self))

    def cmd_RG(self, r, g, b):
        check_error(libfile.a4pdf_dc_cmd_RG(self, r, g, b))

    def cmd_rg(self, r, g, b):
        check_error(libfile.a4pdf_dc_cmd_rg(self, r, g, b))

    def cmd_m(self, x, y):
        check_error(libfile.a4pdf_dc_cmd_m(self, x, y))

    def cmd_re(self, x, y, w, h):
        check_error(libfile.a4pdf_dc_cmd_re(self, x, y, w, h))

    def cmd_w(self, line_width):
        check_error(libfile.a4pdf_dc_cmd_w(self, line_width))

    def cmd_S(self):
        check_error(libfile.a4pdf_dc_cmd_S(self))

    def render_text(self, text, fid, point_size, x, y):
        if not isinstance(text, str):
            raise A4PDFException('Text to render is not a string.')
        if not isinstance(fid, FontId):
            raise A4PDFException('Font id argument is not a font id object.')
        text_bytes = text.encode('UTF-8')
        check_error(libfile.a4pdf_dc_render_utf8_text(self, text_bytes, fid, point_size, x, y))

    def render_text_obj(self, tobj):
        check_error(libfile.a4pdf_dc_render_text_obj(self, tobj))

    def draw_image(self, iid):
        if not isinstance(iid, ImageId):
            raise A4PDFException('Image id argument is not an image id object.')
        check_error(libfile.a4pdf_dc_draw_image(self, iid))

    def translate(self, xtran, ytran):
        self.cmd_cm(1.0, 0, 0, 1.0, xtran, ytran)

    def scale(self, xscale, yscale):
        self.cmd_cm(xscale, 0, 0, yscale, 0, 0)

    def rotate(self, angle):
        self.cmd_cm(math.cos(angle), math.sin(angle), -math.sin(angle), math.cos(angle), 0.0, 0.0)

class StateContextManager:
    def __init__(self, ctx):
        self.ctx = ctx
        ctx.cmd_q()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ctx.cmd_Q()


class Generator:
    def __init__(self, filename, options=None):
        file_name_bytes = to_bytepath(filename)
        if options is None:
            options = Options()
        gptr = ctypes.c_void_p()
        check_error(libfile.a4pdf_generator_new(file_name_bytes, options, ctypes.pointer(gptr)))
        self._as_parameter_ = gptr

    def __del__(self):
        if self._as_parameter_ is not None:
            check_error(libfile.a4pdf_generator_destroy(self))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            self.write()
        else:
            return False

    def page_draw_context(self):
        return DrawContext(self)

    def add_page(self, page_ctx):
        check_error(libfile.a4pdf_generator_add_page(self, page_ctx))

    def embed_jpg(self, fname):
        iid = ImageId()
        check_error(libfile.a4pdf_generator_embed_jpg(self, to_bytepath(fname), ctypes.pointer(iid)))
        return iid

    def load_font(self, fname):
        fid = FontId()
        check_error(libfile.a4pdf_generator_load_font(self, to_bytepath(fname), ctypes.pointer(fid)))
        return fid

    def load_image(self, fname):
        iid = ImageId()
        check_error(libfile.a4pdf_generator_load_image(self, to_bytepath(fname), ctypes.pointer(iid)))
        return iid

    def write(self):
        check_error(libfile.a4pdf_generator_write(self))

class Text:
    def __init__(self):
        self._as_parameter_ = None
        opt = ctypes.c_void_p()
        check_error(libfile.a4pdf_text_new(ctypes.pointer(opt)))
        self._as_parameter_ = opt

    def __del__(self):
        if self._as_parameter_ is not None:
            check_error(libfile.a4pdf_text_destroy(self))

    def render_text(self, text):
        if not isinstance(text, str):
            raise RuntimeError('Text must be a Unicode string.')
        bytes = text.encode('UTF-8')
        check_error(libfile.a4pdf_text_render_utf8_text(self, bytes))

    def cmd_Tc(self, spacing):
        check_error(libfile.a4pdf_text_cmd_Tc(self, spacing))

    def cmd_Td(self, x, y):
        check_error(libfile.a4pdf_text_cmd_Td(self, x, y))

    def cmd_Tf(self, fontid, ptsize):
        if not isinstance(fontid, FontId):
            raise RuntimeError('Font id is not a font object.')
        check_error(libfile.a4pdf_text_cmd_Tf(self, fontid, ptsize))
