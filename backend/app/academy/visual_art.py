"""Original vector pictures tied to the examples, not third-party artwork."""

import re
from html import escape


def icon_for(text):
    words = [
        ("âm thanh|tiếng nói|tiếng chim|giọng nói", "sound"),
        ("mật khẩu|địa chỉ|riêng", "lock"),
        ("ghi nguồn|người vẽ|tác giả|giấy phép", "book"),
        ("công tắc|quạt|theo lệnh", "fan"),
        ("người|bạn|cô|thầy|chào|hello|goodbye", "person"),
        ("mèo|cats?", "cat"),
        ("chó|dogs?", "dog"),
        ("chim|birds?", "bird"),
        ("thỏ|rabbits?", "rabbit"),
        ("cá|fish", "fish"),
        ("rùa|turtles?", "turtle"),
        ("bướm|butterfl(?:y|ies)", "butterfly"),
        ("bò|cows?", "cow"),
        ("cam|oranges?", "orange"),
        ("táo|apples?", "apple"),
        ("chuối|bananas?", "banana"),
        ("lê|pears?", "pear"),
        ("dưa hấu|watermelons?", "watermelon"),
        ("dâu tây|strawberr(?:y|ies)", "strawberry"),
        ("nho|grapes?", "grape"),
        ("dứa|pineapples?", "pineapple"),
        ("sách|books?", "book"),
        ("bút|pencils?", "pencil"),
        ("cặp|bags?", "bag"),
        ("thước|rulers?", "ruler"),
        ("quả bóng|balls?", "ball"),
        ("cốc|cups?", "cup"),
        ("đồng hồ|clocks?", "clock"),
        ("ghế|chairs?", "chair"),
        ("cây|hạt|rau|lá|vườn|tưới", "plant"),
        (r"\d+|đếm|tính|nhóm|mẫu|data", "numbers"),
        ("nhìn|tranh|hình|kiểm tra|đối chiếu|thử", "eye"),
        ("máy|robot", "robot"),
    ]
    ground_truth = re.search(
        r"(?:tranh|ảnh)(?::| là)?\s+(mèo|chó|cam|chim|thỏ|cá)\b", text.casefold()
    )
    if ground_truth:
        return {
            "mèo": "cat",
            "chó": "dog",
            "cam": "orange",
            "chim": "bird",
            "thỏ": "rabbit",
            "cá": "fish",
        }[ground_truth[1]]
    matches = [
        (match.start(), index, icon)
        for index, (pattern, icon) in enumerate(words)
        if (match := re.search(r"(?<!\w)(?:" + pattern + r")(?!\w)", text.casefold()))
    ]
    concrete = [match for match in matches if match[2] not in {"eye", "numbers", "robot"}]
    if matches:
        return min(concrete or matches)[2]
    if re.search(r"(?<!\w)AI(?!\w)", text):
        return "robot"
    return "question" if text.strip().startswith("Ai ") else "idea"


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
    if kind == "sound":
        return path("M45 120H86L133 77V223L86 180H45Z", "#6879cf") + path(
            "M165 111Q199 150 165 189M193 82Q252 150 193 218", stroke="#38a99a", width=10
        )
    if kind == "chair":
        return (
            rect(80, 38, 140, 126, "#d5e3ef", 20)
            + rect(63, 162, 174, 38, "#c68132", 8)
            + path("M83 200V266M217 200V266", stroke="#856b4e", width=13)
        )
    if kind == "question":
        return (
            circle(150, 150, 105, "#d5e3ef")
            + '<text x="150" y="205" text-anchor="middle" font-size="170" fill="#6879cf">?</text>'
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
    match = re.search(r"(?<![\d.,/−-])(\d{1,2})\s*(?:quả và|\+)\s*(\d{1,2})(?![\d.,/])", text)
    return bool(match and int(match[1]) + int(match[2]) <= 20) or bool(
        re.match(r"(?i)(one|two|three)\b", text)
        or re.search(r"(?i)(hai nhóm|ba nhóm|đếm ba quả|đếm mỗi quả|đếm một quả|số lượng 5)", text)
        or re.match(r"\d+(?:,\s*\d+){3};", text)
    )


def labelled_picture(text, variant=0, code=""):
    # Labels remain real SVG text and an accessible caption, never an image of a paragraph.
    from app.academy.media import circle, rect

    body = rect(12, 12, 276, 276, "#edf7f2", 28)
    body += example_art(text, variant)
    if not uses_counters(text):
        body += circle(270, 27, 7 + variant % 4, ["#38a99a", "#f7b84b", "#6879cf"][variant % 3])
    return "<title>" + escape(text) + "</title><desc>" + escape(code) + "</desc>" + body


def example_art(text, variant=0):
    from app.academy.media import OBJECTS, circle, path, rect

    if text == "Nhặt hạt":
        return (
            path("M45 205Q150 274 255 205Z", "#d5e3ef")
            + "".join(
                f'<ellipse cx="{x}" cy="195" rx="13" ry="8" fill="#856b4e"/>'
                for x in (95, 148, 202)
            )
            + path("M65 63L120 108L154 87Q173 81 176 96L140 135Q123 148 109 137L55 99", "#f2c898")
            + '<ellipse cx="156" cy="142" rx="13" ry="8" fill="#856b4e"/>'
        )
    if text == "Gieo hạt":
        return (
            rect(25, 170, 250, 90, "#c9a77d", 8)
            + "".join(
                f'<ellipse cx="{x}" cy="200" rx="13" ry="8" fill="#856b4e"/>'
                for x in (70, 150, 230)
            )
            + path("M150 75V145M138 131L150 145L162 131", stroke="#6879cf", width=8)
        )
    if text in {"Đếm mỗi quả một lần", "Đếm một quả hai lần"}:
        dots = "".join(circle(x, 155, 23, "#38a99a") for x in (60, 150, 240))
        if "hai lần" in text:
            return dots + path(
                "M42 112C-5 35 136 34 84 115M75 97L84 115L102 108", stroke="#c68132", width=7
            )
        return dots + "".join(
            path(f"M{x} 65V111M{x - 9} 99L{x} 111L{x + 9} 99", stroke="#6879cf", width=5)
            for x in (60, 150, 240)
        )
    sequence = re.match(r"(\d+), (\d+), (\d+), (\d+);", text)
    if sequence:
        return "".join(
            circle(48 + i * 67, 150, 26, "#d5e3ef")
            + f'<text x="{48 + i * 67}" y="160" text-anchor="middle" font-size="30" fill="#26475c">{n}</text>'
            for i, n in enumerate(sequence.groups())
        )
    table = re.match(r"Bảng: (\d+), (\d+), (\d+) cây\.", text)
    if table:
        values = [int(n) for n in table.groups()]
        scale = 150 / max(*values, 1)
        return path("M30 235H280M30 235V55", width=3) + "".join(
            rect(48 + i * 77, 230 - n * scale, 45, n * scale, "#38a99a", 0)
            + f'<text x="{70 + i * 77}" y="{220 - n * scale}" text-anchor="middle" font-size="24" fill="#26475c">{n}</text>'
            + f'<text x="{70 + i * 77}" y="266" text-anchor="middle" font-size="20" fill="#26475c">Tổ {i + 1}</text>'
            for i, n in enumerate(values)
        )
    fraction_sum = re.match(r"(\d+)/(\d+)\s*\+\s*(\d+)/(\d+)", text)
    if fraction_sum:
        from fractions import Fraction
        from math import lcm

        a, b, c, d = map(int, fraction_sum.groups())
        if b and d:
            denominator = lcm(b, d)
            if denominator <= 12 and Fraction(a, b) + Fraction(c, d) <= 1:
                first, second = a * denominator // b, c * denominator // d
                return "".join(
                    f'<text x="5" y="{66 + row * 86}" font-size="22" fill="#26475c">{label}</text>'
                    + "".join(
                        rect(
                            65 + i * 210 / denominator,
                            30 + row * 86,
                            210 / denominator - 2,
                            50,
                            "#38a99a" if i < count else "#d5e3ef",
                            0,
                        )
                        for i in range(denominator)
                    )
                    for row, (count, label) in enumerate(
                        (
                            (first, f"{a}/{b}"),
                            (second, f"{c}/{d}"),
                            (first + second, str(Fraction(a, b) + Fraction(c, d))),
                        )
                    )
                )
    percentage = re.match(r"(\d+) trong 100 là", text)
    if percentage and 0 <= int(percentage[1]) <= 100:
        return "".join(
            rect(
                30 + i % 10 * 24,
                25 + i // 10 * 22,
                20,
                18,
                "#38a99a" if i < int(percentage[1]) else "#d5e3ef",
                1,
            )
            for i in range(100)
        )

    # A stated sample is the visual evidence; a later, deliberately wrong claim
    # must not determine the object, quantity or position shown in the picture.
    if text.startswith("Mẫu:"):
        sample = text.split(".", 1)[0].removeprefix("Mẫu:").strip()
        if "two books on desk" in sample:
            return (
                rect(30, 190, 240, 22, "#c68132", 5)
                + path("M55 212V275M245 212V275", stroke="#856b4e", width=9)
                + '<g transform="translate(40 70) scale(.36)">'
                + icon_art("book", variant)
                + "</g>"
                + '<g transform="translate(150 70) scale(.36)">'
                + icon_art("book", variant)
                + "</g>"
            )
        if "cat on chair" in sample:
            return (
                icon_art("chair")
                + '<g transform="translate(65 28) scale(.56)">'
                + icon_art("cat", variant)
                + "</g>"
            )
        return example_art(sample, variant)

    if text.casefold().startswith("tranh: mèo ngồi"):
        return (
            icon_art("chair")
            + '<g transform="translate(65 28) scale(.56)">'
            + icon_art("cat", variant)
            + "</g>"
        )

    fractions = re.search(r"(?:Bánh|Hình) (\d+) (?:phần bằng nhau|ô bằng nhau), chọn (\d+)", text)
    if fractions:
        total, selected = map(int, fractions.groups())
        if 0 <= selected <= total <= 12:
            return "".join(
                rect(
                    25 + i * 250 / total,
                    85,
                    250 / total,
                    120,
                    "#38a99a" if i < selected else "#ffffff",
                    0,
                )
                + path(f"M{25 + i * 250 / total} 85V205", width=2)
                for i in range(total)
            ) + path("M25 85H275V205H25Z", width=3)

    groups = re.search(r"(?i)(hai|ba) nhóm(?:, mỗi nhóm)? (hai|bốn|hai chấm)", text)
    if groups:
        rows = {"hai": 2, "ba": 3}[groups[1].casefold()]
        columns = 4 if groups[2].casefold() == "bốn" else 2
        return "".join(
            rect(30, 25 + row * 85, 240, 70, "#ffffff", 12)
            + "".join(circle(65 + col * 55, 60 + row * 85, 16, "#38a99a") for col in range(columns))
            for row in range(rows)
        )

    if "mèo và chó" in text.casefold() or "mèo hay chó" in text.casefold():
        return (
            '<g transform="translate(0 60) scale(.5)">'
            + icon_art("cat", variant)
            + "</g>"
            + '<g transform="translate(150 60) scale(.5)">'
            + icon_art("dog", variant)
            + "</g>"
        )

    amount = re.match(r"(?i)(?:đếm\s+|số lượng\s+)?(ba|5)\s+(?:quả )?(táo|chiếc bút)", text)
    if amount:
        count = 3 if amount[1].casefold() == "ba" else 5
        icon = "apple" if amount[2].casefold() == "táo" else "pencil"
        return "".join(
            f'<g transform="translate({i % 3 * 95} {i // 3 * 140}) scale(.3)">'
            + icon_art(icon, variant)
            + "</g>"
            for i in range(count)
        )

    if text == "Thẻ bị che kín":
        return (
            rect(55, 35, 190, 230, "#6879cf", 22)
            + path("M63 61L230 228M63 111L197 245M104 47L230 173", stroke="#aeb9ef", width=12)
            + '<text x="150" y="183" text-anchor="middle" font-family="sans-serif" '
            'font-size="100" fill="#ffffff">?</text>'
        )

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
    match = re.search(r"(?<![\d.,/−-])(\d{1,2})\s*(?:quả và|\+)\s*(\d{1,2})(?![\d.,/])", text)
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
            if color_match[1] == "green"
            or (
                color_match[1] == "xanh"
                and (
                    "xanh lá" in text.casefold()
                    or (kind == "apple" and "xanh dương" not in text.casefold())
                )
            )
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
        return (
            "<desc>" + escape(row["visual_prefix"] + f"-{variant}") + "</desc>" + scene(12, variant)
        )
    items = row["activity"]["items"][:3]
    body = (
        "<title>"
        + escape(row["title"])
        + "</title><desc>"
        + escape(row["visual_prefix"] + f"-{variant}")
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
