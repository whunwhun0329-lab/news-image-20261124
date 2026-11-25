#!/usr/bin/env python3
"""Draw the 24 November 2026 one-day world news poster (1024x1024 PNG).

Layout: newspaper front page.
  - masthead + big date line
  - stats strip (5 figures)
  - six main-story panels in a 2x3 grid
  - "in brief" one-line shorts in two columns
  - DATE CHECK box listing stories excluded as other days' news
All copy comes from the date-verified research package for 24 Nov 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
CONTENT_W = W - 2 * MARGIN

FONT_DIR = "/usr/share/fonts/truetype/noto"
F_REG = FONT_DIR + "/NotoSans-Regular.ttf"
F_BOLD = FONT_DIR + "/NotoSans-Bold.ttf"
F_COND = FONT_DIR + "/NotoSans-Condensed.ttf"
F_CONDB = FONT_DIR + "/NotoSans-CondensedBold.ttf"

PAPER = (250, 247, 240)
INK = (20, 18, 14)
ACCENT = (140, 29, 24)
GREY = (96, 92, 84)
RULE = (20, 18, 14)
PANEL_BG = (255, 253, 248)
PANEL_LINE = (198, 190, 172)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_w, line_h, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        assert len(lines) <= max_lines, f"overflow ({len(lines)} lines): {text[:60]}"
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


# ---------------------------------------------------------------- stories

MAINS = [
    {
        "kicker": "UKRAINE  ·  ZAPORIZHZHIA",
        "headline": "Russian Strike on Zaporizhzhia Kills 2, Wounds 40+",
        "detail": (
            "Overnight attack destroyed a house and tore into a five-storey "
            "apartment block. 2 dead, 40+ wounded including 4 children; "
            "rescuers freed 9 people trapped inside."
        ),
        "source": "Source: Reuters",
    },
    {
        "kicker": "INDONESIA  ·  SERANG, BANTEN",
        "headline": "Indonesia Factory Fire Death Toll Rises to 26",
        "detail": (
            "Toll from the Milkita candy-factory fire rose to 26 on Tuesday "
            "as two more bodies were found; 8 workers still missing and "
            "600+ rescuers searching. Police probe opened."
        ),
        "source": "Source: CNA / Police",
    },
    {
        "kicker": "SOUTH KOREA  ·  ULLEUNG ISLAND",
        "headline": "Russian Jets Near Ulleung Island; Korea Issues Rare Alert",
        "detail": (
            "About 5 Russian warplanes entered Korea's air defence zone "
            "over the East Sea; Seoul issued Ulleung Island's first "
            "preliminary air-raid alert and scrambled F-15Ks."
        ),
        "source": "Source: Yonhap",
    },
    {
        "kicker": "SAUDI ARABIA  ·  RIYADH",
        "headline": "Riyadh Finance-District Tower Targeted Again",
        "detail": (
            "Saudi-led coalition says the PIF Tower, the capital's tallest, "
            "was targeted in a terrorist attack on Tuesday. No casualty "
            "figures given; the tower was hit earlier this month."
        ),
        "source": "Source: Reuters",
    },
    {
        "kicker": "AFRICA  ·  SPORT",
        "headline": "Senegal Get AFCON Title Back as CAS Overturns Ruling",
        "detail": (
            "CAS upheld Senegal's appeal, restoring their 1-0 extra-time "
            "AFCON final win over Morocco and overturning CAF's 3-0 "
            "default award, citing breaches of natural justice."
        ),
        "source": "Source: AP",
    },
    {
        "kicker": "UNITED STATES  ·  ECONOMY",
        "headline": "US Consumer Confidence Jumps to 103.3, Highest Since Jan 2025",
        "detail": (
            "Conference Board index leapt 11.4 points to 103.3 in November, "
            "beating every forecast — a 22-month high, credited to "
            "post-election calm and cheaper fuel."
        ),
        "source": "Source: Conference Board via Reuters",
    },
]

STATS = [
    ("26", "DEAD — INDONESIA FIRE TOLL"),
    ("103.3", "US CONSUMER CONFIDENCE, NOV"),
    ("~5", "RUSSIAN JETS IN KOREA'S KADIZ"),
    ("36", "AMAZON LEO SATELLITES LAUNCHED"),
    ("40+", "WOUNDED AT ZAPORIZHZHIA"),
]

SHORTS_LEFT = [
    ("HORMUZ", "Iran claims 3 tankers hit naval mines east of the "
     "strait, even under US escort; talks ruled out until 7 "
     "conditions are met."),
    ("JERUSALEM", "Eisenkot's Yashar clinches first coalition deal "
     "with Lieberman's party; deadline 6 Dec to form a government."),
    ("MINSK", "Lukashenko proposes flying with Zelenskyy to Moscow "
     "for Kremlin talks to end the war."),
    ("GENEVA", "World Chess Championship Game 1 opens: Gukesh, 20, "
     "vs Sindarov, 20; $2.5m prize fund."),
    ("WALL STREET", "Nvidia slips ~5% Tuesday as Monday's record "
     "surge cools; governance risk back in focus."),
]

SHORTS_RIGHT = [
    ("KOUROU", "Ariane 6 flies its 10th mission, lifting 36 Amazon "
     "Leo broadband satellites."),
    ("WASHINGTON", "Kilmar Abrego Garcia agrees to leave the US "
     "voluntarily, ending his deportation fight."),
    ("IOWA", "Federal court clears the Army to detonate ageing toxic "
     "explosives in southeast Iowa."),
    ("AT SEA", "US probes cyberattacks on up to 50 commercial ships "
     "with bomb threats and ransoms (WSJ)."),
]

DATE_CHECK = (
    "Huang's return as Nvidia CEO & +31.5% surge — 23 Nov  ·  Indonesia "
    "factory fire outbreak — 21 Nov  ·  COP31 collapse — 22 Nov  ·  "
    "Democrats' 258-seat House majority — 22 Nov  ·  Alcaraz's ATP Finals "
    "title — 22 Nov  ·  BepiColombo reaches Mercury — 21 Nov  ·  "
    "Verstappen's Las Vegas GP win — 21 Nov"
)


# ---------------------------------------------------------------- drawing

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(F_CONDB, 21)
    f_date = font(F_BOLD, 50)
    f_sub = font(F_REG, 15)
    f_stat_num = font(F_BOLD, 29)
    f_stat_lab = font(F_CONDB, 12)
    f_kicker = font(F_CONDB, 13)
    f_head = font(F_BOLD, 19)
    f_detail = font(F_REG, 13)
    f_source = font(F_REG, 11)
    f_sec = font(F_CONDB, 19)
    f_short_lab = font(F_CONDB, 13)
    f_short = font(F_REG, 13)
    f_dc_head = font(F_CONDB, 14)
    f_dc = font(F_REG, 13)

    # ---- masthead
    y = 14
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    badge = "15 STORIES"
    bw = d.textlength(badge, font=f_mast) + 20
    d.rectangle([W - MARGIN - bw, y - 2, W - MARGIN, y + 28], fill=ACCENT)
    d.text((W - MARGIN - bw + 10, y + 2), badge, font=f_mast, fill=(255, 255, 255))
    d.line([MARGIN, y + 34, W - MARGIN, y + 34], fill=RULE, width=3)

    # ---- date line
    y = 54
    d.text((MARGIN, y), "TUESDAY 24 NOVEMBER 2026", font=f_date, fill=INK)
    y = 114
    d.text(
        (MARGIN, y),
        "One day of world news: events that happened, or were first "
        "reported, on 24 November 2026.",
        font=f_sub, fill=GREY,
    )
    d.line([MARGIN, y + 22, W - MARGIN, y + 22], fill=RULE, width=1)

    # ---- stats strip
    y = 146
    cell_w = CONTENT_W / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        d.text((cx + 4, y), num, font=f_stat_num, fill=ACCENT)
        draw_wrapped(d, (cx + 4, y + 36), lab, f_stat_lab, INK, cell_w - 12, 14,
                     max_lines=2)
        if i:
            d.line([cx - 6, y + 2, cx - 6, y + 58], fill=PANEL_LINE, width=1)
    d.line([MARGIN, y + 66, W - MARGIN, y + 66], fill=RULE, width=2)

    # ---- main panels, 2 cols x 3 rows
    top = 224
    gap = 9
    col_w = (CONTENT_W - gap) / 2
    panel_h = 140
    for idx, story in enumerate(MAINS):
        row, col = divmod(idx, 2)
        px = MARGIN + col * (col_w + gap)
        py = top + row * (panel_h + gap)
        d.rectangle([px, py, px + col_w, py + panel_h], fill=PANEL_BG,
                    outline=PANEL_LINE, width=1)
        # kicker bar
        d.rectangle([px, py, px + col_w, py + 20], fill=ACCENT)
        d.text((px + 10, py + 3), story["kicker"], font=f_kicker,
               fill=(255, 255, 255))
        # headline
        hy = draw_wrapped(d, (px + 10, py + 25), story["headline"], f_head,
                          INK, col_w - 20, 23, max_lines=2)
        # detail
        draw_wrapped(d, (px + 10, hy + 1), story["detail"], f_detail,
                     INK, col_w - 20, 17, max_lines=3)
        # source pinned to panel bottom
        d.text((px + 10, py + panel_h - 15), story["source"], font=f_source,
               fill=GREY)

    # ---- shorts
    y = top + 3 * panel_h + 2 * gap + 12
    d.text((MARGIN, y), "AROUND THE WORLD — IN BRIEF", font=f_sec, fill=INK)
    d.line([MARGIN, y + 24, W - MARGIN, y + 24], fill=RULE, width=1)
    y += 32
    short_col_w = (CONTENT_W - gap) / 2
    draw_shorts(d, y, short_col_w, gap, f_short_lab, f_short)

    # ---- date check box
    box_y = 908
    d.rectangle([MARGIN, box_y, W - MARGIN, box_y + 82], outline=ACCENT, width=2)
    d.text((MARGIN + 12, box_y + 8),
           "DATE CHECK — DELIBERATELY EXCLUDED: NOT 24 NOVEMBER NEWS",
           font=f_dc_head, fill=ACCENT)
    draw_wrapped(d, (MARGIN + 12, box_y + 32), DATE_CHECK, f_dc, INK,
                 CONTENT_W - 24, 18, max_lines=3)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


def draw_shorts(d, y, col_w, gap, f_lab, f_body):
    """Two columns of one-line briefs; label inline on the first line."""
    for col_idx, shorts in enumerate((SHORTS_LEFT, SHORTS_RIGHT)):
        sx = MARGIN + col_idx * (col_w + gap)
        sy = y
        for label, text in shorts:
            lab = label + " — "
            lw = d.textlength(lab, font=f_lab)
            d.text((sx, sy), lab, font=f_lab, fill=ACCENT)
            # first line uses the width left of the label; later lines full
            words = text.split()
            lines = []
            cur = ""
            limit = col_w - lw
            for word in words:
                trial = word if not cur else cur + " " + word
                if d.textlength(trial, font=f_body) <= limit:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = word
                    limit = col_w
            if cur:
                lines.append(cur)
            assert len(lines) <= 2, f"short overflow ({len(lines)}): {label}"
            for j, line in enumerate(lines):
                lx = sx + lw if j == 0 else sx
                d.text((lx, sy + j * 17), line, font=f_body, fill=INK)
            sy += len(lines) * 17 + 6


if __name__ == "__main__":
    main()
