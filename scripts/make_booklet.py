#!/usr/bin/env python3

import argparse
import copy
import math
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject


PT_PER_MM = 72.0 / 25.4


def mm_to_pt(mm: float) -> float:
    return mm * PT_PER_MM


def normalize_page(page: PageObject) -> PageObject:
    """
    Copy a page and bake its /Rotate value into the page contents, so that
    width/height and transformations behave predictably.
    """
    p = copy.copy(page)
    p.transfer_rotation_to_content()
    return p


def place_page(
    sheet: PageObject,
    src: PageObject,
    slot_x: float,
    slot_y: float,
    slot_w: float,
    slot_h: float,
    margin: float = 0.0,
) -> None:
    """
    Place src page into the given rectangular slot on sheet, uniformly scaled
    and centered.
    """
    usable_w = slot_w - 2 * margin
    usable_h = slot_h - 2 * margin

    if usable_w <= 0 or usable_h <= 0:
        raise ValueError("Margin is too large for the target slot.")

    src_box = src.mediabox
    src_x0 = float(src_box.left)
    src_y0 = float(src_box.bottom)
    src_w = float(src_box.width)
    src_h = float(src_box.height)

    scale = min(usable_w / src_w, usable_h / src_h)

    scaled_w = src_w * scale
    scaled_h = src_h * scale

    tx = slot_x + margin + (usable_w - scaled_w) / 2
    ty = slot_y + margin + (usable_h - scaled_h) / 2

    transform = (
        Transformation()
        .translate(tx=-src_x0, ty=-src_y0)
        .scale(sx=scale, sy=scale)
        .translate(tx=tx, ty=ty)
    )

    sheet.merge_transformed_page(src, transform, expand=False)


def booklet_order(total_pages: int):
    """
    Yield pairs of imposed sheet pages.

    For 4 pages:
      front: left=4, right=1
      back:  left=2, right=3

    Returned indices are zero-based.
    """
    for sheet_index in range(total_pages // 4):
        front_left = total_pages - 1 - 2 * sheet_index
        front_right = 2 * sheet_index

        back_left = 2 * sheet_index + 1
        back_right = total_pages - 2 - 2 * sheet_index

        yield (front_left, front_right)
        yield (back_left, back_right)


def make_booklet(
    input_pdf: Path,
    output_pdf: Path,
    sheet_width_mm: float = 297.0,
    sheet_height_mm: float = 210.0,
    margin_mm: float = 0.0,
) -> None:
    """
    Create an A4-landscape booklet PDF.

    sheet_width_mm=297 and sheet_height_mm=210 means A4 landscape.
    Each half of the sheet is A5 portrait.
    """
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    source_pages = [normalize_page(p) for p in reader.pages]
    original_count = len(source_pages)

    if original_count == 0:
        raise ValueError("Input PDF has no pages.")

    padded_count = int(math.ceil(original_count / 4) * 4)

    sheet_w = mm_to_pt(sheet_width_mm)
    sheet_h = mm_to_pt(sheet_height_mm)
    margin = mm_to_pt(margin_mm)

    # Two A5 portrait slots on one A4 landscape sheet.
    panel_w = sheet_w / 2.0
    panel_h = sheet_h

    for left_index, right_index in booklet_order(padded_count):
        sheet = PageObject.create_blank_page(width=sheet_w, height=sheet_h)

        # Left panel.
        if left_index < original_count:
            place_page(
                sheet,
                source_pages[left_index],
                slot_x=0,
                slot_y=0,
                slot_w=panel_w,
                slot_h=panel_h,
                margin=margin,
            )

        # Right panel.
        if right_index < original_count:
            place_page(
                sheet,
                source_pages[right_index],
                slot_x=panel_w,
                slot_y=0,
                slot_w=panel_w,
                slot_h=panel_h,
                margin=margin,
            )

        writer.add_page(sheet)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Wrote booklet PDF: {output_pdf}")
    print(f"Original pages: {original_count}")
    print(f"Padded to:      {padded_count}")
    print(f"Output pages:   {padded_count // 2}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a portrait PDF into an A4-landscape saddle-stitch booklet PDF."
    )
    parser.add_argument("input", type=Path, help="Input PDF")
    parser.add_argument("output", type=Path, help="Output booklet PDF")
    parser.add_argument(
        "--margin-mm",
        type=float,
        default=0.0,
        help="Optional margin inside each A5 panel, in millimetres. Default: 0",
    )
    parser.add_argument(
        "--sheet-width-mm",
        type=float,
        default=297.0,
        help="Output sheet width in mm. Default: 297, A4 landscape width",
    )
    parser.add_argument(
        "--sheet-height-mm",
        type=float,
        default=210.0,
        help="Output sheet height in mm. Default: 210, A4 landscape height",
    )

    args = parser.parse_args()

    make_booklet(
        input_pdf=args.input,
        output_pdf=args.output,
        sheet_width_mm=args.sheet_width_mm,
        sheet_height_mm=args.sheet_height_mm,
        margin_mm=args.margin_mm,
    )


if __name__ == "__main__":
    main()