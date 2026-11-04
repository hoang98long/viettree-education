export type LearningRelease = { code: string; title: string };

export function ReleaseFilter({
  releases,
  value,
  onChange,
}: {
  releases: LearningRelease[];
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label>
      Bộ bài học
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Tất cả bộ bài</option>
        {releases.map((release) => (
          <option key={release.code} value={release.code}>
            {release.title}
          </option>
        ))}
      </select>
    </label>
  );
}
