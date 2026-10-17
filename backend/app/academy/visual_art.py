"""Original vector pictures tied to the examples, not third-party artwork."""

import re
from html import escape


def icon_for(text):
    words = [
        ("mật khẩu|địa chỉ|riêng|nguồn", "lock"),
        ("công tắc|quạt|theo lệnh", "fan"),
        ("người|bạn|cô|thầy|chào|hello|goodbye", "person"),
        ("mèo|cats?", "cat"),
        ("chó|dogs?", "dog"),
        ("cam|orange", "orange"),
        ("táo|apple", "apple"),
        ("sách|book", "book"),
        ("bút|pencil", "pencil"),
        ("cặp|bag", "bag"),
        ("cây|hạt|rau", "plant"),
        (r"\d+|đếm|tính|nhóm|mẫu|data", "numbers"),
        ("nhìn|tranh|hình|kiểm tra|đối chiếu|thử", "eye"),
        ("máy|robot|ai", "robot"),
    ]
    ground_truth = re.search(r"(?:tranh|ảnh) (?:là )?(mèo|chó|cam)\b", text.casefold())
    if ground_truth:
        return {"mèo": "cat", "chó": "dog", "cam": "orange"}[ground_truth[1]]
    matches = [
        (match.start(), index, icon)
        for index, (pattern, icon) in enumerate(words)
        if (match := re.search(r"(?<!\w)(?:" + pattern + r")(?!\w)", text.casefold()))
    ]
    concrete = [match for match in matches if match[2] not in {"eye", "numbers", "robot"}]
    return min(concrete or matches)[2] if matches else "idea"


def icon_art(kind, variant=0):
    from app.academy.media import OBJECTS, circle, object_art, path, rect, robot

    if kind in {code for code, _, _ in OBJECTS}:
        return object_art(kind, variant)
    if kind == "robot":
        return robot(variant)
    if kind == "person":
        return (
            circle(150, 90, 42, "#f2c898")
            + path("M75 244V190Q150 120 225 190V244Z", "#6879cf")
            + path("M125 104Q150 123 175 104", width=3)
        )
    if kind == "fan":
        return (
            circle(150, 126, 82, "#e9f4ff")
            + circle(150, 126, 14, "#26475c")
            + "".join(
                f'<g transform="rotate({angle} 150 126)">'
                + path("M150 112Q100 30 80 84Q63 134 135 137Z", "#45a7cb")
                + "</g>"
                for angle in [0, 120, 240]
            )
            + path("M150 208V251M104 252H196")
        )
    if kind == "lock":
        return (
            path("M98 116V88Q98 25 150 25Q202 25 202 88V116", stroke="#26475c", width=14)
            + rect(65, 110, 170, 140, "#f7b84b", 24)
            + circle(150, 161, 14, "#26475c")
            + path("M150 174V199", width=9)
        )
    if kind == "plant":
        return (
            path("M150 256V104", stroke="#23805b", width=9)
            + path("M150 145Q58 147 73 80Q128 66 150 145", "#83af56")
            + path("M150 112Q210 37 244 91Q237 145 150 112", "#38a99a")
            + path("M82 258H224", stroke="#c68132")
        )
    if kind == "eye":
        return (
            path("M30 150Q150 14 270 150Q150 286 30 150Z", "#ffffff", "#45a7cb", 9)
            + circle(150, 150, 51, "#6879cf")
            + circle(150, 150, 20, "#26475c")
        )
    if kind == "numbers":
        return (
            rect(58, 25, 184, 245, "#6879cf", 24)
            + rect(82, 49, 136, 64, "#ffffff", 10)
            + "".join(
                rect(83 + i * 49, 137 + j * 48, 32, 32, "#f7b84b" if i == 2 else "#e8f4ee", 7)
                for j in range(2)
                for i in range(3)
            )
            + path("M135 72H165M150 58V87", stroke="#23805b", width=5)
        )
    if kind == "sun":
        return circle(150, 150, 63, "#f7b84b") + "".join(
            f'<g transform="rotate({angle} 150 150)">'
            + path("M150 36V13", stroke="#f7b84b", width=9)
            + "</g>"
            for angle in range(0, 360, 45)
        )
    if kind == "house":
        return (
            rect(72, 126, 157, 128, "#bce4ed", 10)
            + path("M43 137L150 46L258 137Z", "#dc788d")
            + rect(127, 182, 43, 72, "#f7b84b")
            + rect(89, 158, 27, 31, "#ffffff")
        )
    return (
        circle(150, 118, 70, "#f7d675")
        + rect(118, 198, 64, 25, "#6879cf")
        + path("M122 248H178M120 38L100 13M180 38L200 13M64 115H28M238 115H274", stroke="#c68132")
    )


def uses_counters(text):
    match = re.search(r"(?<![\d.,−-])(\d{1,2})\s*(?:quả và|\+)\s*(\d{1,2})(?![\d.,])", text)
    return bool(match and int(match[1]) + int(match[2]) <= 20)


def labelled_picture(text, variant=0, code=""):
    # Labels remain real SVG text and an accessible caption, never an image of a paragraph.
    from app.academy.media import circle, rect

    body = rect(12, 12, 276, 276, "#edf7f2", 28)
    body += example_art(text, variant)
    if not uses_counters(text):
        body += circle(270, 27, 7 + variant % 4, ["#38a99a", "#f7b84b", "#6879cf"][variant % 3])
    return "<title>" + escape(text) + "</title><desc>" + escape(code) + "</desc>" + body


def example_art(text, variant=0):
    from app.academy.media import OBJECTS, circle

    kind = icon_for(text)
    count = re.match(r"(?i)(one|two|three)\b", text)
    if count:
        number = {"one": 1, "two": 2, "three": 3}[count[1].lower()]
        if kind in {code for code, _, _ in OBJECTS}:
            return "".join(
                f'<g transform="translate({i * 300 / number} {30 if number > 1 else 0}) scale({1 / number})">'
                + icon_art(kind, variant)
                + "</g>"
                for i in range(number)
            )
        return "".join(
            circle(150 + (i - (number - 1) / 2) * 65, 150, 24, "#38a99a") for i in range(number)
        )
    match = re.search(r"(?<![\d.,−-])(\d{1,2})\s*(?:quả và|\+)\s*(\d{1,2})(?![\d.,])", text)
    if match and int(match[1]) + int(match[2]) <= 20:
        a, b = int(match[1]), int(match[2])
        return "".join(
            circle(40 + i % 5 * 54, 65 + i // 5 * 55, 16, "#38a99a" if i < a else "#f7b84b")
            for i in range(a + b)
        )
    art = icon_art(kind, variant)
    color_match = re.search(r"(?<!\w)(đỏ|red|xanh|green|blue)(?!\w)", text.casefold())
    if color_match and kind in {code for code, _, _ in OBJECTS}:
        from app.academy.media import COLORS

        colors = [COLORS[variant % len(COLORS)]]
        if kind == "pencil":
            colors.append("#f0bc58")
        if kind == "apple":
            colors.append("#ed8a7d")
        target = (
            "#e87969"
            if color_match[1] in {"đỏ", "red"}
            else "#83af56"
            if color_match[1] == "green" or (color_match[1] == "xanh" and kind == "apple")
            else "#45a7cb"
        )
        for color in colors:
            art = art.replace(f'fill="{color}"', f'fill="{target}"').replace(
                f'stroke="{color}"', f'stroke="{target}"'
            )
    return art


def lesson_scene(row, variant=0):
    from app.academy.media import circle, path, rect, scene

    if row["grade"] == 4 and row["number"] == 12:
        return "<desc>" + escape(row["code"] + f"-v2-{variant}") + "</desc>" + scene(12, variant)
    items = row["activity"]["items"][:3]
    body = (
        "<title>"
        + escape(row["title"])
        + "</title><desc>"
        + escape(row["code"] + f"-v2-{variant}")
        + "</desc>"
    )
    body += rect(10, 10, 580, 340, "#edf7f2", 28)
    width = 540 / len(items)
    for i, item in enumerate(items):
        x = 30 + i * width
        body += rect(x, 45, width - 12, 235, "#ffffff", 20)
        scale = (width - 20) / 300
        body += (
            f'<g transform="translate({x + 4} 50) scale({scale})">'
            + example_art(item["text"], variant)
            + "</g>"
        )
        label = item["text"]
        # Keep the complete accessible title; show a short name under the drawing.
        words, lines, line = label.split(), [], ""
        for word in words:
            if len(line + " " + word) > (18 if len(items) == 2 else 13):
                lines.append(line)
                line = word
            else:
                line = (line + " " + word).strip()
        lines.append(line)
        for j, text in enumerate(lines[:3]):
            body += f'<text x="{x + (width - 12) / 2}" y="{258 + j * 26}" font-family="sans-serif" font-size="20" fill="#26475c" text-anchor="middle">{escape(text)}</text>'
        if variant and not uses_counters(item["text"]):
            body += circle(x + width - 32, 65, 10, ["#38a99a", "#f7b84b", "#6879cf"][variant - 1])
    if len(items) == 2:
        body += path("M281 148H313M305 140L313 148L305 156", stroke="#6879cf", width=3)
    return body
