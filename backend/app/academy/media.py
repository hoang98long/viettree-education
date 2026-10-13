"""Thư viện SVG nguyên bản, biểu đồ học thuật và kiểm tra manifest."""

import hashlib
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from xml.etree import ElementTree

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
MANIFEST = ROOT / "data/media-manifest.json"
COLORS = ["#38a99a", "#f7b84b", "#6879cf", "#dc788d", "#45a7cb", "#83af56"]
OBJECTS = [
    ("cat", "Mèo", "Con vật"),
    ("dog", "Chó", "Con vật"),
    ("rabbit", "Thỏ", "Con vật"),
    ("fish", "Cá", "Con vật"),
    ("bird", "Chim", "Con vật"),
    ("turtle", "Rùa", "Con vật"),
    ("butterfly", "Bướm", "Con vật"),
    ("cow", "Bò", "Con vật"),
    ("apple", "Táo", "Trái cây"),
    ("banana", "Chuối", "Trái cây"),
    ("orange", "Cam", "Trái cây"),
    ("pear", "Lê", "Trái cây"),
    ("watermelon", "Dưa hấu", "Trái cây"),
    ("strawberry", "Dâu tây", "Trái cây"),
    ("grape", "Nho", "Trái cây"),
    ("pineapple", "Dứa", "Trái cây"),
    ("book", "Sách", "Đồ dùng"),
    ("pencil", "Bút chì", "Đồ dùng"),
    ("bag", "Cặp sách", "Đồ dùng"),
    ("cup", "Cốc", "Đồ dùng"),
    ("ruler", "Thước", "Đồ dùng"),
    ("ball", "Bóng", "Đồ dùng"),
    ("scissors", "Kéo dùng có người lớn hướng dẫn", "Đồ dùng"),
    ("clock", "Đồng hồ", "Đồ dùng"),
]


def uid(code):
    return uuid5(NAMESPACE_URL, "viettree:ai-academy:" + code)


def circle(x, y, r, fill):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def rect(x, y, w, h, fill, radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"/>'


def path(d, fill="none", stroke="#284a61", width=5):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def robot(expression=0):
    body = rect(75, 70, 150, 120, "#54bca7", 28) + rect(91, 87, 118, 70, "#f8fffd", 20)
    body += (
        rect(103, 185, 94, 66, "#7cccbc", 20)
        + rect(88, 241, 34, 16, "#335f76")
        + rect(178, 241, 34, 16, "#335f76")
    )
    body += path("M150 70 V43") + circle(150, 35, 12, "#f5c85c")
    if expression in (2, 6):
        body += path("M112 112 Q125 101 138 112 M162 112 Q175 101 188 112")
    else:
        body += circle(125, 114, 7 if expression != 4 else 11, "#284a61") + circle(
            175, 114, 7 if expression != 4 else 11, "#284a61"
        )
    mouths = [
        "M136 139 Q150 151 165 139",
        "M136 141 H164",
        "M135 137 Q150 153 165 137",
        "M137 143 Q150 135 163 143",
        "M143 138 Q150 153 157 138",
        "M139 141 L151 134 L164 141",
        "M136 136 Q150 150 164 136",
        "M139 141 H162",
    ]
    body += path(mouths[expression % 8], width=3)
    body += path("M75 193 L47 213" if expression % 2 else "M75 192 L45 169")
    body += path("M225 193 L249 163" if expression < 4 else "M225 193 L258 215")
    body += circle(145, 211, 8, "#ffe0a6")
    if expression == 5:
        body += path("M30 112 L44 125 L67 97", stroke="#288b73")
    if expression == 7:
        body += rect(228, 90, 40, 47, "#ffdc8c") + path("M248 102 V117 M248 128 V129")
    return body


def object_art(kind, variant=0):
    c = COLORS[variant % len(COLORS)]
    if kind in {"cat", "dog", "rabbit", "cow"}:
        ears = path("M93 103 L100 62 L129 95 M171 95 L202 62 L207 107", c)
        if kind == "rabbit":
            ears = rect(101, 27, 25, 84, c) + rect(174, 27, 25, 84, c)
        if kind in {"dog", "cow"}:
            ears = path("M93 101 L58 108 L71 159 L112 122", c) + path(
                "M189 102 L241 109 L224 159 L189 125", c
            )
        value = (
            ears
            + rect(92, 91, 114, 120, c, 45)
            + circle(124, 133, 6, "#26475c")
            + circle(176, 133, 6, "#26475c")
        )
        value += path("M138 163 Q151 177 166 162") + circle(151, 154, 8, "#294b61")
        if kind == "cat":
            value += path(
                "M85 156 L118 160 M86 175 L118 171 M184 160 L218 154 M184 172 L217 180", width=3
            )
        if kind == "cow":
            value += circle(126, 180, 13, "#f5e9d8") + circle(184, 102, 14, "#f5e9d8")
        return value
    if kind == "fish":
        return (
            path("M200 146 L254 95 L254 199 Z", c)
            + f'<ellipse cx="141" cy="148" rx="75" ry="49" fill="{c}"/>'
            + circle(106, 137, 6, "#284a61")
            + path("M130 99 L165 76 L179 108", c)
        )
    if kind == "bird":
        return (
            circle(143, 143, 65, c)
            + path("M206 135 L243 149 L206 162", "#f6bd57")
            + circle(175, 118, 6, "#284a61")
            + path("M83 147 Q131 105 167 149 Q136 190 96 182", "#bce4ed")
            + path("M130 207 V233 M163 207 V233")
        )
    if kind == "turtle":
        return (
            circle(221, 166, 28, "#8caf61")
            + f'<ellipse cx="145" cy="154" rx="78" ry="52" fill="{c}"/>'
            + path(
                "M95 126 L120 155 L153 115 L178 155 L201 130 M120 155 L145 189 L178 155",
                stroke="#e6f7cc",
                width=4,
            )
            + circle(233, 159, 4, "#284a61")
        )
    if kind == "butterfly":
        return (
            circle(110, 119, 43, c)
            + circle(193, 119, 43, "#f4b267")
            + circle(115, 179, 36, "#c88fd0")
            + circle(189, 179, 36, c)
            + rect(146, 95, 13, 119, "#345775", 6)
            + path("M152 97 L133 70 M152 97 L173 70")
        )
    if kind in {"apple", "orange", "pear", "strawberry", "pineapple"}:
        fills = {
            "apple": "#ed8a7d",
            "orange": "#f4ac48",
            "pear": "#b0c975",
            "strawberry": "#dc758c",
            "pineapple": "#e7c474",
        }
        body = (
            circle(150, 160, 68, fills[kind])
            if kind != "pear"
            else path(
                "M150 74 Q185 90 181 122 Q231 184 190 224 Q109 253 88 191 Q78 156 120 116 Q118 81 150 74",
                fills[kind],
            )
        )
        if kind == "apple":
            body = path(
                "M150 99 Q90 61 80 145 Q76 222 138 229 Q149 218 166 229 Q232 217 222 146 Q218 63 150 99",
                fills[kind],
            )
        elif kind == "strawberry":
            body = path("M90 107 Q150 76 213 109 Q204 190 151 243 Q98 194 90 107", fills[kind])
        elif kind == "pineapple":
            body = rect(98, 98, 109, 147, fills[kind], 40)
        body += path("M153 91 V65")
        body += path("M154 77 Q190 42 207 75 Q183 95 154 77", "#72ab71", "#72ab71")
        if kind in {"strawberry", "pineapple"}:
            body += "".join(
                circle(118 + i * 25, 142 + j * 26, 3, "#fff6cb") for i in range(3) for j in range(3)
            )
        return body
    if kind == "banana":
        return path("M68 101 Q130 178 226 90 Q229 202 130 228 Q72 211 68 101", "#f4cc67") + path(
            "M82 121 Q113 192 202 139", stroke="#c9a443", width=3
        )
    if kind == "watermelon":
        return (
            path("M62 100 H240 Q227 249 151 244 Q69 232 62 100", "#91bd7b")
            + path("M80 113 H222 Q208 220 151 225 Q94 217 80 113", "#df8694")
            + "".join(
                circle(x, y, 4, "#375268")
                for x, y in [(112, 142), (153, 151), (192, 142), (135, 190), (169, 190)]
            )
        )
    if kind == "grape":
        return "".join(
            circle(100 + i * 34 + j * 17, 113 + j * 34, 20, "#aa8cc7")
            for j in range(4)
            for i in range(4 - j)
        ) + path("M147 95 V sixty".replace(" sixty", "60"))
    if kind == "book":
        return (
            path(
                "M45 84 Q103 61 150 91 Q204 64 258 85 V217 Q201 193 150 222 Q95 194 45 215 Z",
                "#f0ce82",
            )
            + path("M150 91 V219")
            + path(
                "M67 116 H124 M67 141 H124 M176 116 H235 M176 141 H235", stroke="#fff6db", width=6
            )
        )
    if kind == "pencil":
        return (
            path("M61 213 L188 57 L229 88 L103 243 Z", "#f0bc58")
            + path("M61 213 L48 261 L103 243", "#ebdac5")
            + path("M61 213 L188 57", stroke=c, width=8)
        )
    if kind == "bag":
        return (
            path("M112 77 Q111 38 184 77", stroke="#446984", width=10)
            + rect(79, 72, 141, 165, c, 28)
            + rect(103, 153, 93, 65, "#ffe2a6", 14)
            + path("M101 113 H199", stroke="#f5fffb")
        )
    if kind == "cup":
        return (
            path("M200 110 Q270 104 245 178 Q222 197 200 184", stroke=c, width=14)
            + rect(81, 97, 125, 127, c, 20)
            + path("M87 101 Q143 123 201 101", stroke="#f1fffc", width=6)
        )
    if kind == "ruler":
        return rect(45, 115, 220, 66, "#f4d37e") + "".join(
            path(f"M{x} 119 V{146 if i % 2 else 156}", width=3)
            for i, x in enumerate(range(59, 260, 20))
        )
    if kind == "ball":
        return (
            circle(152, 151, 84, "#87b9dd")
            + path("M148 125 L181 146 L169 181 L130 181 L119 146 Z", "#f7e2ae")
            + path(
                "M67 151 H116 M188 145 L236 124 M132 185 L114 225 M170 186 L195 224",
                stroke="#fff9e6",
                width=7,
            )
        )
    if kind == "scissors":
        return (
            circle(95, 205, 27, c)
            + circle(158, 209, 27, c)
            + path("M108 185 L203 54 M152 184 L75 50", stroke="#7195af", width=14)
            + circle(128, 156, 7, "#f9db8c")
        )
    return (
        circle(151, 151, 85, c)
        + circle(151, 151, 68, "#fff7e6")
        + path("M151 108 V152 L187 179", width=7)
        + "".join(
            circle(x, y, 4, "#49637c") for x, y in [(151, 98), (204, 151), (151, 204), (98, 151)]
        )
    )


def scene(number, variant=0):
    # Mỗi cảnh bám nhiệm vụ bài: bộ dữ liệu, phân số, nguồn, truyện, poster hoặc dự án.
    value = rect(22, 22, 556, 316, "#f0faf6", 28)
    if number == 12:
        import math

        parts, selected = (8, 3) if variant in (0, 3) else (4, 1)
        for i in range(parts):
            a, b = i * 2 * math.pi / parts, (i + 1) * 2 * math.pi / parts
            x1, y1 = 165 + 104 * math.sin(a), 180 - 104 * math.cos(a)
            x2, y2 = 165 + 104 * math.sin(b), 180 - 104 * math.cos(b)
            value += path(
                f"M165 180 L{x1:.2f} {y1:.2f} A104 104 0 0 1 {x2:.2f} {y2:.2f} Z",
                "#efb35d" if i < selected else "#d7e8de",
                "#ffffff",
                3,
            )
        value += "".join(
            rect(
                320 + i % 4 * 42,
                130 + i // 4 * 52,
                38,
                48,
                "#efb35d" if i < selected else "#d7e8de",
                3,
            )
            for i in range(parts)
        )
    elif number in {5, 6, 19, 33}:
        kinds = (
            ["cat", "bird", "rabbit", "dog"]
            if number == 5
            else ["cat", "cat", "cat", "bird"]
            if number == 6
            else ["apple", "bird", "ruler", "pear"]
            if number == 33
            else ["book", "pencil", "apple", "bag"]
        )
        for i, kind in enumerate(kinds):
            value += f'<g transform="translate({55 + (i % 2) * 280},{40 + (i // 2) * 155}) scale(.48)">{object_art(kind, variant + i)}</g>'
        if variant == 2:
            value += path("M280 90 L302 110 L332 60", stroke="#d58a58")
    elif number == 14:
        for box in range(36):
            x, y = 37 + (box % 9) * 58, 46 + (box // 9) * 70
            value += rect(x, y, 52, 62, "#d6e8f3", 6)
            value += "".join(
                circle(x + 12 + (k % 5) * 7, y + 14 + (k // 5) * 8, 2.4, COLORS[variant % 6])
                for k in range(25)
            )
    elif number in {11, 13}:
        for box in range(6):
            x, y = 65 + (box % 3) * 165, 66 + (box // 3) * 135
            value += rect(x, y, 145, 110, "#d6e8f3", 16)
            value += "".join(
                circle(
                    x + 35 + (k % 2) * 65,
                    y + 32 + (k // 2) * 44,
                    11,
                    "#ecb264" if variant % 2 == 0 else "#7bb89f",
                )
                for k in range(4)
            )
        if number == 13:
            value += path("M40 182 H554", stroke="#795f46", width=8)
    elif number == 16:
        value += f'<g transform="translate(30,55) scale(.82)">{robot(variant)}</g>'
        value += (
            circle(366, 134, 34, "#d8a486")
            + rect(329, 166, 76, 105, "#7d9fc9", 26)
            + path("M342 268 V299 M389 268 V299", width=13)
        )
        value += (
            path("M486 301 V181", stroke="#856b4e", width=15)
            + circle(486, 137, 54, "#8abc79")
            + circle(448, 169, 37, "#91c58e")
        )
    elif number == 24:
        for frame in range(4):
            x = 36 + frame * 136
            value += rect(x, 63, 126, 234, ["#e3f1ef", "#fff0ce", "#dfedf8", "#ede3f1"][frame], 12)
            value += f'<g transform="translate({x + 17},{120 + (frame % 2) * 18}) scale(.32)">{robot((frame + variant) % 8)}</g>'
            value += path(f"M{x + 95} 270 V235", stroke="#71a779", width=7) + circle(
                x + 97, 218 + frame * 4, 14 + frame * 3, "#84b788"
            )
            value += rect(x + 16, 79, 90, 26, "#ffffff", 9)
    elif number in {23, 30}:
        value += f'<g transform="translate(148,35) scale(1.04)">{robot((number + variant) % 8)}</g>'
        value += circle(80, 180, 37, "#ffe0a4") + path("M61 181 L77 198 L106 160", stroke="#498e72")
    elif number in {27, 28, 29}:
        value += rect(95, 92, 197, 162, "#d0e6ef", 18) + rect(116, 119, 154, 89, "#ffffff", 8)
        if number == 27:
            value += (
                path("M362 157 V128 Q400 88 434 130 V158", stroke="#5b8ea0", width=12)
                + rect(340, 148, 119, 107, "#80bdaa", 18)
                + circle(399, 190, 11, "#315572")
                + rect(394, 192, 10, 27, "#315572", 3)
            )
        elif number == 28:
            value += (
                circle(391, 158, 61, "#fcddb2")
                + circle(391, 158, 40, "#e8f5f6")
                + path("M431 198 L484 252", stroke="#4b748c", width=20)
            )
            value += (
                f'<g transform="translate(142,125) scale(.25)">{object_art("cat", variant)}</g>'
            )
        else:
            value += (
                f'<g transform="translate(335,98) scale(.66)">{object_art("book", variant)}</g>'
            )
            value += path("M138 232 H249 M350 264 H479", stroke="#8aa0b4", width=8)
    elif number in {7, 8, 9, 10, 15, 17, 18, 20, 21, 22}:
        for i in range(3 if variant != 2 else 4):
            x = 45 + i * 135
            value += rect(x, 70 + (i % 2) * 40, 115, 143, "#ffffff", 17) + circle(
                x + 57, 113 + (i % 2) * 40, 19, COLORS[(number + i) % 6]
            )
            value += path(f"M{x + 20} {160 + (i % 2) * 40} H{x + 95}", stroke="#8bafb4", width=5)
            if i < 2:
                value += path(
                    f"M{x + 118} 266 H{x + 131} M{x + 123} 259 L{x + 131} 266 L{x + 123} 273",
                    stroke="#5c9c8f",
                    width=4,
                )
        if number in {18, 19, 22}:
            value += (
                f'<g transform="translate(435,162) scale(.43)">{object_art("book", variant)}</g>'
            )
        elif number == 21:
            value += path(
                "M420 155 Q490 100 500 170 Q499 202 468 206 Q445 209 462 237",
                stroke="#6e84b5",
                width=9,
            )
        elif number == 20:
            value += (
                circle(479, 195, 27, "#d9a785")
                + rect(447, 226, 64, 66, "#88b3cd", 20)
                + rect(446, 171, 65, 16, "#614d49", 8)
            )
        elif number == 15:
            value += path("M495 285 V200", stroke="#856b4e", width=13) + circle(
                495, 167, 49, "#91be86"
            )
    elif number in {25, 31, 32, 34, 35, 36}:
        value += rect(73, 44, 300, 267, "#ffffff", 19) + rect(91, 63, 264, 49, "#d4ede3", 12)
        for i in range(3):
            value += rect(
                100, 132 + i * 47, 135 + (variant + i) % 3 * 29, 18, COLORS[(number + i) % 6], 7
            )
            value += circle(331, 140 + i * 47, 12, "#cce9da")
        value += f'<g transform="translate(360,106) scale(.64)">{robot((number + variant) % 8)}</g>'
        if number == 25:
            value += path("M259 126 Q230 161 262 172 Q299 160 259 126", "#78b4cc", "#78b4cc")
    else:
        value += f'<g transform="translate(128,31) scale(.9)">{robot((number + variant) % 8)}</g>'
        for i, kind in enumerate(["book", "apple", "clock"]):
            value += f'<g transform="translate({35 + i * 172},200) scale(.38)">{object_art(kind, variant + i)}</g>'
        if number == 26:
            value += rect(452, 62, 95, 95, "#f5d08a", 18) + "".join(
                circle(x, y, 8, "#597591")
                for x, y in [(476, 87), (521, 87), (498, 109), (476, 135), (521, 135)]
            )
    if variant:
        value += path("M38 323 H560", stroke=COLORS[variant], width=5)
        # Support roles: compare/check/explain with distinct geometry, not renamed copies.
        value += circle(545, 48, 14 + variant * 2, COLORS[variant])
    return value


def svg(content, width=600, height=360):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">{content}</svg>'


def generate(records):
    from app.academy.visual_art import labelled_picture, lesson_scene

    ASSETS.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    # Retain previous media bytes/hashes: historical versions still reference them.
    assets = json.loads(MANIFEST.read_text(encoding="utf-8"))["assets"] if MANIFEST.exists() else []
    existing = {asset["code"] for asset in assets}

    def add(code, category, alt, body, width=600, height=360):
        if code in existing:
            return
        raw = svg(body, width, height).encode("utf-8")
        filename = code + ".svg"
        (ASSETS / filename).write_bytes(raw)
        assets.append(
            dict(
                id=str(uid(code)),
                code=code,
                category=category,
                alt=alt,
                file=filename,
                width=width,
                height=height,
                sha256=hashlib.sha256(raw).hexdigest(),
                bytes=len(raw),
                license="CC BY 4.0 · VietTree Education · minh họa nguyên bản",
                source="SVG do VietTree biên soạn bằng code",
            )
        )
        existing.add(code)

    for i, name in enumerate(
        [
            "chào",
            "đang đọc",
            "vui khi thử lại",
            "đang nghĩ",
            "ngạc nhiên",
            "kiểm tra",
            "chúc mừng",
            "nhắc an toàn",
        ]
    ):
        add(
            f"mascot-{i}",
            "mascot",
            f"Robot Mầm AI {name}; nhân vật minh họa không có cảm xúc thật",
            robot(i),
            300,
            300,
        )
    for i, (kind, name, label) in enumerate(OBJECTS):
        for variant in range(3):
            add(
                f"card-{kind}-{variant}",
                "card",
                f"Thẻ {name}, biến thể màu và bối cảnh {variant + 1}",
                rect(5, 5, 290, 290, ["#edf7ee", "#f8f0df", "#edf0fa"][variant], 24)
                + object_art(kind, variant),
                300,
                300,
            )
    for i in range(12):
        star = path(
            "M150 58 L172 111 L231 116 L187 156 L198 215 L150 187 L103 215 L113 156 L69 116 L128 111 Z",
            COLORS[i % 6],
            COLORS[i % 6],
        )
        add(
            f"badge-{i}",
            "badge",
            f"Huy hiệu khám phá {i + 1}: ghi nhận quá trình học",
            circle(150, 147, 108, "#eef5ed")
            + star
            + circle(150, 148, 21, "#fff7d6")
            + path(f"M{118 + i} 150 L144 169 L{175 + i} 126", stroke="#588974"),
            300,
            300,
        )
        add(
            f"ui-{i}",
            "ui",
            [
                "Bắt đầu",
                "Tiếp tục",
                "Thử lại",
                "Kiểm tra nguồn",
                "Giữ riêng",
                "Đã lưu",
                "Chờ giáo viên",
                "Làm từng bước",
                "Đã hiểu",
                "Cần trợ giúp",
                "Kết nối lại",
                "Nghỉ một chút",
            ][i],
            rect(12, 12, 276, 276, "#e7f4ef", 32)
            + robot(i % 8)
            + circle(42 + i * 5, 43, 14, COLORS[i % 6]),
            300,
            300,
        )
    covers = set()
    for record in records:
        code = record["visual_prefix"]
        if record["unit_code"] not in covers:
            covers.add(record["unit_code"])
            add(
                "cover-" + record["unit_code"],
                "cover",
                f"Chủ đề {record['unit_title']}: tình huống học bằng tranh",
                lesson_scene(record, 0)
                + path("M40 38 H220", stroke=COLORS[record["grade"] % 6], width=8),
            )
        add(
            code + "-hero",
            "hero",
            f"Tình huống: {record['title']}",
            lesson_scene(record, 0)
            + circle(562, 325, 9 + record["grade"], COLORS[record["grade"] % 6]),
        )
        for variant, purpose in enumerate(
            ["Quan sát và tìm đặc điểm", "Đối chiếu một trường hợp khác", "Kiểm tra và vận dụng"], 1
        ):
            add(
                code + f"-support-{variant}",
                "illustration",
                f"{record['title']} · {purpose}",
                lesson_scene(record, variant)
                + rect(27, 27, 5 + record["grade"] * 3, 14, "#98c7bb", 3),
            )
        for i, item in enumerate(record["activity"]["items"], 1):
            item_code = code + f"-item-{i}"
            add(
                item_code,
                "illustration",
                item["text"],
                labelled_picture(item["text"], i, item_code),
                300,
                300,
            )
    manifest = {
        "assets": assets,
        "lessons": {
            r["code"]: {
                "cover": "cover-" + r["unit_code"],
                "hero": r["visual_prefix"] + "-hero",
                "illustrations": [r["visual_prefix"] + f"-support-{i}" for i in range(1, 4)],
                "cards": r["cards"],
            }
            for r in records
        },
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def validate_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    hashes = set()
    for asset in manifest["assets"]:
        raw = (ASSETS / asset["file"]).read_bytes()
        ElementTree.fromstring(raw)
        if (
            not asset["alt"].strip()
            or len(raw) > 150000
            or hashlib.sha256(raw).hexdigest() != asset["sha256"]
        ):
            raise ValueError(f"Asset chưa hợp lệ: {asset['code']}")
        if asset["sha256"] in hashes:
            raise ValueError(f"Asset trùng nội dung: {asset['code']}")
        hashes.add(asset["sha256"])
    codes = {a["code"] for a in manifest["assets"]}
    for mapping in manifest["lessons"].values():
        if (
            not {mapping["cover"], mapping["hero"], *mapping["illustrations"], *mapping["cards"]}
            <= codes
        ):
            raise ValueError("Manifest thiếu media")
    return {
        "assets": len(hashes),
        "lessons": len(manifest["lessons"]),
        "categories": {
            c: sum(a["category"] == c for a in manifest["assets"])
            for c in {a["category"] for a in manifest["assets"]}
        },
    }
