// Original vector pictures for concrete primary-school vocabulary.
// Run with: node scripts/generate-learning-pictures.mjs
import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath, URL } from "node:url";
import console from "node:console";

const target = new URL("../public/learning/", import.meta.url);
mkdirSync(target, { recursive: true });
const art = {
  pen: [
    "Bút mực",
    '<path d="M37 123L54 90L109 30L129 49L75 109Z" fill="#76afb9"/><path d="M37 123L75 109L54 90Z" fill="#d8eef4"/><path d="M37 123L44 114M99 42L117 59M102 36L93 25L74 46" fill="none"/>',
  ],
  schoolbag: [
    "Cặp sách",
    '<path d="M58 38V28Q80 10 102 28V38" fill="none"/><rect x="34" y="36" width="92" height="106" rx="22" fill="#e87969"/><rect x="49" y="88" width="62" height="36" rx="10" fill="#ffe3a3"/><path d="M54 62H106"/>',
  ],
  ruler: [
    "Thước kẻ",
    '<rect x="17" y="52" width="126" height="57" rx="8" fill="#ffe3a3"/><path d="M32 54V78M48 54V69M64 54V78M80 54V69M96 54V78M112 54V69M128 54V78"/>',
  ],
  eraser: [
    "Cục tẩy",
    '<path d="M30 100L58 47H113L136 72L105 121H53Z" fill="#e879a7"/><path d="M79 47L104 72L73 121H53L30 100L58 47Z" fill="#f8ede5"/><path d="M104 72H136"/>',
  ],
  desk: [
    "Bàn học",
    '<rect x="18" y="49" width="124" height="24" rx="6" fill="#eac18d"/><path d="M32 73V132M126 73V132"/><rect x="85" y="73" width="43" height="27" rx="4" fill="#eac18d"/><path d="M100 84H111"/>',
  ],
  chair: [
    "Ghế",
    '<rect x="46" y="22" width="68" height="64" rx="9" fill="#eac18d"/><rect x="38" y="84" width="84" height="19" rx="5" fill="#eac18d"/><path d="M49 103V140M110 103V140M59 39V65M80 39V65M101 39V65"/>',
  ],
  school: [
    "Trường học",
    '<path d="M16 64L80 20L144 64Z" fill="#e87969"/><rect x="25" y="64" width="110" height="75" fill="#ffe3a3"/><rect x="66" y="97" width="28" height="42" fill="#79aabb"/><rect x="41" y="79" width="15" height="23" fill="#d8eef4"/><rect x="104" y="79" width="15" height="23" fill="#d8eef4"/><circle cx="80" cy="50" r="13" fill="#fff"/><path d="M80 42V50L86 54"/>',
  ],
  bus: [
    "Xe buýt",
    '<rect x="15" y="45" width="130" height="70" rx="13" fill="#f2c663"/><path d="M24 90H136"/><rect x="27" y="57" width="23" height="26" rx="3" fill="#cfe8f5"/><rect x="57" y="57" width="23" height="26" rx="3" fill="#cfe8f5"/><rect x="87" y="57" width="23" height="26" rx="3" fill="#cfe8f5"/><rect x="119" y="57" width="17" height="48" rx="3" fill="#cfe8f5"/><circle cx="43" cy="115" r="15" fill="#486578"/><circle cx="116" cy="115" r="15" fill="#486578"/>',
  ],
  bicycle: [
    "Xe đạp",
    '<circle cx="35" cy="112" r="26" fill="#fff"/><circle cx="126" cy="112" r="26" fill="#fff"/><path d="M35 112L65 65L84 112H35L104 65L126 112M84 112L65 65M58 65H73M104 65L96 44H114" fill="none" stroke="#e87969" stroke-width="7"/>',
  ],
  car: [
    "Ô tô",
    '<path d="M19 90L37 82L54 51H104L127 82L142 88V114H19Z" fill="#76afb9"/><path d="M60 62H96L113 82H50Z" fill="#d8eef4"/><circle cx="46" cy="114" r="16" fill="#486578"/><circle cx="117" cy="114" r="16" fill="#486578"/>',
  ],
  rain: [
    "Mưa",
    '<path d="M39 80A20 20 0 0 1 41 42A29 29 0 0 1 95 37A23 23 0 0 1 128 80Z" fill="#b5d4e2"/><path d="M46 99L37 117M81 99L72 117M116 99L107 117M55 124L49 137M98 124L92 137" stroke="#5794be" stroke-width="6"/>',
  ],
  cloud: [
    "Đám mây",
    '<path d="M33 106A24 24 0 0 1 34 61A33 33 0 0 1 97 52A29 29 0 0 1 131 106Z" fill="#d4e8f0"/>',
  ],
  flower: [
    "Bông hoa",
    '<path d="M80 80V140M80 116Q35 116 51 94Q74 89 80 116M80 126Q126 121 113 102Q89 99 80 126" fill="#79b695"/><g fill="#e879a7"><ellipse cx="80" cy="37" rx="17" ry="24"/><ellipse cx="109" cy="61" rx="24" ry="17"/><ellipse cx="96" cy="88" rx="17" ry="24" transform="rotate(-30 96 88)"/><ellipse cx="64" cy="88" rx="17" ry="24" transform="rotate(30 64 88)"/><ellipse cx="51" cy="61" rx="24" ry="17"/></g><circle cx="80" cy="64" r="20" fill="#ffe3a3"/>',
  ],
  milk: [
    "Sữa",
    '<path d="M46 45L61 21H102L116 45V140H46Z" fill="#fff"/><path d="M46 45H116M61 21V45"/><rect x="47" y="74" width="68" height="43" fill="#b5d4e2"/><path d="M79 84Q55 109 79 109Q101 109 79 84Z" fill="#fff"/>',
  ],
  water: [
    "Nước uống",
    '<path d="M39 38H121L111 137H49Z" fill="#d8eef4"/><path d="M44 81Q62 69 80 81T116 81L111 137H49Z" fill="#76badd"/><path d="M60 47L63 70" stroke="#fff"/>',
  ],
  bread: [
    "Bánh mì",
    '<path d="M25 87Q16 67 39 51Q80 25 123 54Q146 74 135 91L124 132H36Z" fill="#eac18d"/><path d="M48 62L42 86M75 52L69 78M103 61L97 84" stroke="#a57648"/>',
  ],
  egg: [
    "Quả trứng",
    '<path d="M37 99Q34 60 64 25Q80 9 96 25Q126 60 123 99Q119 143 80 143Q41 143 37 99Z" fill="#fff7e7"/><path d="M52 97Q49 77 64 57" stroke="#fff" stroke-width="8"/>',
  ],
  circle: ["Hình tròn", '<circle cx="80" cy="80" r="54" fill="#76afb9"/>'],
  square: [
    "Hình vuông",
    '<rect x="27" y="27" width="106" height="106" fill="#79b695"/>',
  ],
  triangle: ["Hình tam giác", '<path d="M80 22L139 133H21Z" fill="#ffe3a3"/>'],
  rectangle: [
    "Hình chữ nhật",
    '<rect x="16" y="42" width="128" height="76" fill="#e879a7"/>',
  ],
};
for (const [name, label, fill] of [
  ["red", "Màu đỏ", "#e87969"],
  ["blue", "Màu xanh dương", "#5b94dc"],
  ["green", "Màu xanh lá", "#56a36f"],
  ["yellow", "Màu vàng", "#f5d15f"],
  ["purple", "Màu tím", "#9c78bf"],
  ["pink", "Màu hồng", "#e88fb4"],
  ["brown", "Màu nâu", "#98704f"],
  ["black", "Màu đen", "#263439"],
  ["white", "Màu trắng", "#ffffff"],
])
  art[`color-${name}`] = [
    label,
    `<circle cx="80" cy="80" r="54" fill="${fill}"/>`,
  ];

for (const [code, [label, drawing]] of Object.entries(art)) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="160" height="160"><title>${label}</title><rect width="160" height="160" rx="24" fill="#f1f8f3"/><g stroke="#486578" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">${drawing}</g></svg>\n`;
  writeFileSync(new URL(`${code}.svg`, target), svg, "utf8");
}
console.log(
  `Generated ${Object.keys(art).length} original pictures in ${fileURLToPath(target)}`,
);
