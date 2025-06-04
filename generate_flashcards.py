from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import Color, HexColor
import os
import re

# ---------------- CONFIGURATION ----------------
FONT_PATH = "NotoSansSC-Regular.ttf"
FONT_NAME = "NotoSansSC"

# FONT_PATH = "NotoSerifSC-Regular.ttf"
# FONT_NAME = "NotoSerifSC"

LANGUAGE = "es"

# PAGESIZE = "A3"
PAGESIZE = "A4"

MARGIN_MM = 4

HANZI_FONT_SIZE = 34
PINYIN_FONT_SIZE = 14
MEANING_FONT_SIZE = 8

PINYIN_OFFSET = 6
MEANING_OFFSET = 8

TRIANGLE_SIZE = 35
HSK_COLORS = {
    1: '#fbff00',
    2: '#4bea00',
    3: '#00ffff',
    4: '#0097ff',
    5: '#fb00ff',
    6: '#ff0000'
}

if PAGESIZE == "A4":
    PAGE_HEIGHT, PAGE_WIDTH = A4
    ROWS = 5
    COLS = 6
elif PAGESIZE == "A3":
    PAGE_WIDTH, PAGE_HEIGHT = A3
    ROWS = 10
    COLS = 6

MARGIN = MARGIN_MM * mm
# ------------------------------------------------

USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN
USABLE_HEIGHT = PAGE_HEIGHT - 2 * MARGIN

CELL_WIDTH = USABLE_WIDTH / COLS
CELL_HEIGHT = USABLE_HEIGHT / ROWS

pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

def parse_file(file_path):
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            hanzi, pinyin, meaning = line.split('\t')
            entries.append((hanzi, pinyin, meaning))
    return entries

def draw_centered_text(c, text, x, y, width, height, font_size):
    c.setFont(FONT_NAME, font_size)

    if "…" in text and text.count("…") >= 2:
        parts = text.split("…")
        chunks = []
        i = 0
        while i < len(parts) - 1:
            left = parts[i].strip()
            right = parts[i + 1].strip()
            if left:
                chunks.append(left + "…")
            if right:
                chunks.append(right + "…")
            i += 2
        if len(parts) % 2 == 1 and parts[-1].strip():
            chunks.append(parts[-1].strip())

        lines = chunks[:2] if len(chunks) >= 2 else [text]
        total_height = len(lines) * font_size * 1.3
        start_y = y + (1.25 * height - total_height) / 2 + font_size

        for i, line in enumerate(lines):
            text_width = pdfmetrics.stringWidth(line, FONT_NAME, font_size)
            text_x = x + (width - text_width) / 2
            text_y = start_y - i * font_size * 1.3
            c.drawString(text_x, text_y, line)
    else:
        text_width = pdfmetrics.stringWidth(text, FONT_NAME, font_size)
        text_x = x + (width - text_width) / 2
        text_y = y + (height - font_size) / 2
        c.drawString(text_x, text_y, text)

def draw_hsk_tag(c, x, y, hsk_level):
    color = HSK_COLORS.get(hsk_level, Color(0.5,0.5,0.5))
    c.setFillColor(HexColor(color))
    c.setStrokeColor(HexColor(color))

    path = c.beginPath()
    path.moveTo(x, y + CELL_HEIGHT)
    path.lineTo(x, y + CELL_HEIGHT - TRIANGLE_SIZE)
    path.lineTo(x + TRIANGLE_SIZE, y + CELL_HEIGHT)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    c.setFont(FONT_NAME, 8)
    c.setFillColor(Color(0,0,0))
    c.drawString(x + 3, y + CELL_HEIGHT - 12, f"HSK{hsk_level}")

def draw_grid(c):
    c.setStrokeColor(Color(0.9,0.9,0.9))
    c.setDash(1, 2)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_WIDTH + MARGIN
            y = row * CELL_HEIGHT + MARGIN
            c.rect(x, y, CELL_WIDTH, CELL_HEIGHT)

def create_flashcards_pdf(entries, filename, hsk_level):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    num_cards = ROWS * COLS
    total_pages = (len(entries) + num_cards - 1) // num_cards

    for page in range(total_pages):
        page_entries = entries[page * num_cards:(page + 1) * num_cards]

        # Front face
        for index, (hanzi, _, _) in enumerate(page_entries):
            row = index // COLS
            col = index % COLS
            x = col * CELL_WIDTH + MARGIN
            y = (ROWS - 1 - row) * CELL_HEIGHT + MARGIN
            draw_centered_text(c, hanzi, x, y, CELL_WIDTH, CELL_HEIGHT, HANZI_FONT_SIZE)
        draw_grid(c)
        c.showPage()

        # Back face
        for index, (_, pinyin, meaning) in enumerate(page_entries):
            row = index // COLS
            col = COLS - 1 - (index % COLS)
            x = col * CELL_WIDTH + MARGIN
            y = (ROWS - 1 - row) * CELL_HEIGHT + MARGIN

            draw_hsk_tag(c, x, y, hsk_level)

            c.setFont(FONT_NAME, PINYIN_FONT_SIZE)
            text_width = pdfmetrics.stringWidth(pinyin, FONT_NAME, PINYIN_FONT_SIZE)
            text_x = x + (CELL_WIDTH - text_width) / 2
            text_y = y + CELL_HEIGHT - PINYIN_FONT_SIZE - PINYIN_OFFSET - 5
            c.drawString(text_x, text_y, pinyin)

            c.setFont(FONT_NAME, MEANING_FONT_SIZE)
            wrapped = wrap_text(meaning, CELL_WIDTH - 4, MEANING_FONT_SIZE)
            total_height = len(wrapped) * MEANING_FONT_SIZE * 1.2
            start_y = y + (CELL_HEIGHT - total_height) / 2 - MEANING_OFFSET
            for i, line in enumerate(wrapped):
                line_width = pdfmetrics.stringWidth(line, FONT_NAME, MEANING_FONT_SIZE)
                line_x = x + (CELL_WIDTH - line_width) / 2
                line_y = start_y + (len(wrapped) - 1 - i) * MEANING_FONT_SIZE * 1.2
                c.drawString(line_x, line_y, line)

        draw_grid(c)
        c.showPage()
    c.save()

def wrap_text(text, max_width, font_size):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test_line = current + " " + word if current else word
        width = pdfmetrics.stringWidth(test_line, FONT_NAME, font_size)
        if width <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

if __name__ == "__main__":
    for lvl in range(1, 7):
        input_file = f"./txt/{LANGUAGE}/hsk_{lvl}_{LANGUAGE}.txt"
        output_pdf = f"./pdf/{PAGESIZE}/{LANGUAGE}/hsk_{lvl}_{LANGUAGE}_{PAGESIZE}_flashcards.pdf"
        os.makedirs(os.path.split(output_pdf)[0],exist_ok=True)
        entries = parse_file(input_file)
        create_flashcards_pdf(entries, output_pdf, lvl)
        print(f"PDF generated: {output_pdf}")
