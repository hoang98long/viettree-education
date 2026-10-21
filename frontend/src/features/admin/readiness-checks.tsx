import styles from "./readiness-checks.module.css";

export type ReadinessCheck = {
  code: string;
  label: string;
  ok: boolean;
  count: number | null;
};

export function ReadinessChecks({
  checks,
  label,
}: {
  checks: ReadinessCheck[];
  label: string;
}) {
  return (
    <ul className={styles.checks} aria-label={label}>
      {checks.map((check) => (
        <li key={check.code}>
          <span>{check.label}</span>
          <strong className={check.ok ? styles.passed : styles.attention}>
            {check.ok ? "Đạt" : "Cần xử lý"}
            {check.count !== null ? ` · ${check.count}` : ""}
          </strong>
        </li>
      ))}
    </ul>
  );
}
