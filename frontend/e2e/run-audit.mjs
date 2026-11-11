import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import process from "node:process";

const fixtureFile = process.env.E2E_FIXTURE_FILE;
if (!fixtureFile)
  throw new Error(
    "Cần E2E_FIXTURE_FILE từ prepare_e2e trên database test riêng",
  );
const raw = readFileSync(fixtureFile);
const text = raw
  .toString(raw[0] === 255 && raw[1] === 254 ? "utf16le" : "utf8")
  .replace(/^\uFEFF/, "");
const fixtures = JSON.parse(text);
const env = {
  ...process.env,
  ...fixtures,
  E2E_ADMIN_PASSWORD:
    process.env.E2E_ADMIN_PASSWORD || process.env.SEED_ADMIN_PASSWORD,
  E2E_STUDENT_PASSWORD:
    process.env.E2E_STUDENT_PASSWORD || process.env.SEED_STUDENT_PASSWORD,
};
const required = [
  "E2E_ADMIN_PASSWORD",
  "E2E_STUDENT_PASSWORD",
  "E2E_STUDENT_USERNAME",
  "E2E_AUTHORING_STUDENT_USERNAME",
  "E2E_ACADEMY_DESKTOP_USERNAME",
  "E2E_ACADEMY_MOBILE_USERNAME",
  "E2E_EDITORIAL_GRADE4_FREE_DESKTOP_USERNAME",
  "E2E_EDITORIAL_GRADE4_FREE_MOBILE_USERNAME",
];
for (const grade of [1, 2, 3, 4, 5])
  for (const plan of ["FREE", "VIP"])
    for (const device of ["DESKTOP", "MOBILE"])
      required.push(`E2E_EDITORIAL_GRADE${grade}_${plan}_${device}_USERNAME`);
for (const device of ["DESKTOP", "MOBILE"]) {
  required.push(`E2E_VISUAL_GRADE4_${device}_USERNAME`);
  required.push(`E2E_AUDIT_SUBMIT_${device}_USERNAME`);
  required.push(`E2E_COLOR_${device}_USERNAME`);
  required.push(`E2E_PICTURE_${device}_USERNAME`);
}
for (const name of required)
  if (!env[name]) throw new Error(`Thiếu fixture bắt buộc: ${name}`);
const files = process.argv.slice(2);
const selected = files.some(
  (file) => file.endsWith(".spec.ts") || file === "e2e",
)
  ? files
  : [
      "e2e/sessions.spec.ts",
      "e2e/attempt-autosave.spec.ts",
      "e2e/authoring.spec.ts",
      "e2e/editorial-review.spec.ts",
      "e2e/audit-accessibility.spec.ts",
      ...files,
    ];
const result = spawnSync(
  process.execPath,
  [
    "node_modules/@playwright/test/cli.js",
    "test",
    "--forbid-only",
    ...selected,
  ],
  { env, stdio: "inherit" },
);
if (result.error) throw result.error;
process.exit(result.status ?? 1);
