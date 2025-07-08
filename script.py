from fpdf import FPDF
import csv


# Load from csv
def load_data_from_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            name = row[0].strip()
            team_id = row[1].strip().upper()
            data.append((name, team_id))
    return data


print("Setting up basics...")

# Dimensions
CARD_H = 55
CARD_W = 85
PAGE_H = 297
PAGE_W = 210
BORDER_W = 2

MARGIN_X = (PAGE_W - 2 * CARD_W) / 2
MARGIN_Y = (PAGE_H - 4 * CARD_H) / 2

pdf = FPDF(format="A4")
print("Loading fonts...")
pdf.add_font("EnglishFont", "", "fonts/AoboshiOne-Regular(Font).ttf", uni=True)
pdf.add_font("MandarinFont", "", "fonts/LXGWWenKaiTC-Bold.ttf", uni=True)

csv_file = "filename.csv"
print(f"Loading data from {csv_file}...")

# Sample data
data = load_data_from_csv(csv_file)

# Counter
i = 0

print("Creating the pdf of cards...")
# For every page
for name, team in data:
    if i % 8 == 0:
        pdf.add_page()

    pos = i % 8
    row = pos // 2
    col = pos % 2
    # x, y pos with offset
    x = MARGIN_X + col * CARD_W
    y = MARGIN_Y + row * CARD_H + (row * BORDER_W / 2)

    if i % 2 == 1:
        x += BORDER_W / 2
    if (i % 8 == 0) or (i == len(data)):
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(1.0)

        for col in range(0, 3):
            line_x = MARGIN_X - 0.5 + col * (CARD_W + BORDER_W / 2)
            pdf.line(line_x, MARGIN_Y, line_x, MARGIN_Y +
                     4 * CARD_H + 1.75 * BORDER_W)

        for row in range(0, 6):
            line_y = MARGIN_Y - 0.5 + row * (CARD_H + BORDER_W / 2)
            pdf.line(MARGIN_X - 0.5, line_y, MARGIN_X + 2 *
                     CARD_W + BORDER_W * 0.75, line_y)

    # Draw card background
    pdf.image("namecard.png", x, y, CARD_W, CARD_H)

    # Team ID
    if team.lower() in ['a', 'b', "c", "d", "e", "f", "g", "h"]:
        pdf.set_font("EnglishFont", size=24)
        pdf.set_xy(x + 15, y + 8)
        pdf.cell(CARD_W, CARD_H // 2 + 5, f"{team}", align='L', ln=False)
    else:
        pdf.set_font("MandarinFont", size=18)
        pdf.set_xy(x + 14, y - 2)
        pdf.cell(CARD_W, CARD_H // 2 + 5, f"{team}", align='C', ln=False)

    pdf.set_font("EnglishFont", size=12)
    pdf.image("logo.png", x + 43, y + CARD_H / 2 + 12, 12, 12)

    # IONC Wording
    pdf.set_xy(x + 20, y + CARD_H / 2 + 8)
    pdf.cell(CARD_W, CARD_H // 2 - 5, "IONC", align='C', ln=False)

    # Name
    if team.lower() != "staff":
        pdf.set_xy(x + 14, y + 11)
    else:
        pdf.set_xy(x + 14, y + 13)

    pdf.set_font("MandarinFont", size=38)
    pdf.cell(CARD_W, CARD_H // 2 + 5, f"{name}", align='C', ln=False)

    i += 1

print("Output pdf: cards.pdf")
pdf.output("cards.pdf")
print("Success!")
