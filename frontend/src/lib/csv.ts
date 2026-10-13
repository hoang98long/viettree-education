/** Excel-friendly CSV; text cells cannot become spreadsheet formulas. */
export function csvDocument(rows: readonly (readonly (string | number)[])[]) {
  return (
    "\uFEFF" +
    rows
      .map((row) =>
        row
          .map((cell) => {
            let value = String(cell);
            let start = 0;
            while (
              start < value.length &&
              (value.charCodeAt(start) <= 32 || /\s/.test(value[start]))
            )
              start++;
            if (typeof cell === "string" && /^[=+@-]/.test(value.slice(start)))
              value = "'" + value;
            return '"' + value.replaceAll('"', '""') + '"';
          })
          .join(","),
      )
      .join("\r\n") +
    "\r\n"
  );
}

export function downloadCsv(
  filename: string,
  rows: readonly (readonly (string | number)[])[],
) {
  const url = URL.createObjectURL(
    new Blob([csvDocument(rows)], { type: "text/csv;charset=utf-8" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
