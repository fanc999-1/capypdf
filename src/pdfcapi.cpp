/*
 * Copyright 2023 Jussi Pakkanen
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <a4pdf.h>
#include <pdfgen.hpp>
#include <pdfdrawcontext.hpp>
#include <errors.hpp>

using namespace A4PDF;

A4PDF_EC a4pdf_options_new(A4PDF_Options **out_ptr) A4PDF_NOEXCEPT {
    *out_ptr = reinterpret_cast<A4PDF_Options *>(new PdfGenerationData());
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_options_destroy(A4PDF_Options *opt) A4PDF_NOEXCEPT {
    delete reinterpret_cast<PdfGenerationData *>(opt);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_options_set_title(A4PDF_Options *opt, const char *utf8_title) A4PDF_NOEXCEPT {
    reinterpret_cast<PdfGenerationData *>(opt)->title = utf8_title;
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_PUBLIC A4PDF_EC a4pdf_options_set_mediabox(
    A4PDF_Options *opt, double x, double y, double w, double h) A4PDF_NOEXCEPT {
    auto opts = reinterpret_cast<PdfGenerationData *>(opt);
    opts->mediabox.x = x;
    opts->mediabox.y = y;
    opts->mediabox.w = w;
    opts->mediabox.h = h;
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_generator_add_page(A4PDF_Generator *g, A4PDF_DrawContext *dctx) A4PDF_NOEXCEPT {
    auto *gen = reinterpret_cast<PdfGen *>(g);
    auto *ctx = reinterpret_cast<PdfDrawContext *>(dctx);
    gen->add_page(*ctx);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_PUBLIC A4PDF_EC a4pdf_generator_load_font(A4PDF_Generator *g,
                                                const char *fname,
                                                A4PDF_FontId *fid) A4PDF_NOEXCEPT {
    auto *gen = reinterpret_cast<PdfGen *>(g);
    *fid = gen->load_font(fname);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_generator_new(const char *filename,
                             const A4PDF_Options *options,
                             A4PDF_Generator **out_ptr) A4PDF_NOEXCEPT {
    auto opts = reinterpret_cast<const PdfGenerationData *>(options);
    *out_ptr = reinterpret_cast<A4PDF_Generator *>(new PdfGen(filename, *opts));
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_generator_destroy(A4PDF_Generator *generator) A4PDF_NOEXCEPT {
    delete reinterpret_cast<PdfGen *>(generator);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC a4pdf_page_draw_context_new(A4PDF_Generator *g,
                                     A4PDF_DrawContext **out_ptr) A4PDF_NOEXCEPT {
    auto *gen = reinterpret_cast<PdfGen *>(g);
    *out_ptr = reinterpret_cast<A4PDF_DrawContext *>(gen->new_page_draw_context());
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_PUBLIC A4PDF_EC a4pdf_dc_render_utf8_text(A4PDF_DrawContext *ctx,
                                                const char *text,
                                                A4PDF_FontId fid,
                                                double point_size,
                                                double x,
                                                double y) A4PDF_NOEXCEPT {
    auto c = reinterpret_cast<PdfDrawContext *>(ctx);
    c->render_utf8_text(text, fid, point_size, x, y);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC
a4pdf_dc_set_rgb_stroke(A4PDF_DrawContext *ctx, double r, double g, double b) A4PDF_NOEXCEPT {
    auto c = reinterpret_cast<PdfDrawContext *>(ctx);
    DeviceRGBColor rgb{r, g, b};
    c->set_stroke_color(rgb);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC
a4pdf_dc_set_rgb_nonstroke(A4PDF_DrawContext *ctx, double r, double g, double b) A4PDF_NOEXCEPT {
    auto c = reinterpret_cast<PdfDrawContext *>(ctx);
    DeviceRGBColor rgb{r, g, b};
    c->set_nonstroke_color(rgb);
    return (A4PDF_EC)ErrorCode::NoError;
}

A4PDF_EC
a4pdf_dc_cmd_re(A4PDF_DrawContext *ctx, double x, double y, double w, double h) A4PDF_NOEXCEPT {
    auto c = reinterpret_cast<PdfDrawContext *>(ctx);
    return (A4PDF_EC)c->cmd_re(x, y, w, h);
}

A4PDF_EC a4pdf_dc_cmd_f(A4PDF_DrawContext *ctx) A4PDF_NOEXCEPT {
    auto c = reinterpret_cast<PdfDrawContext *>(ctx);
    return (A4PDF_EC)c->cmd_f();
}

A4PDF_EC a4pdf_dc_destroy(A4PDF_DrawContext *ctx) A4PDF_NOEXCEPT {
    delete reinterpret_cast<PdfDrawContext *>(ctx);
    return (A4PDF_EC)ErrorCode::NoError;
}

const char *a4pdf_error_message(A4PDF_EC error_code) A4PDF_NOEXCEPT {
    return error_text((ErrorCode)error_code);
}
