"use client";
import { useState } from "react";
import { api } from "@/lib/api";
import { useResource } from "@/hooks/use-resource";
import { Loading, ErrorState, PageTitle } from "@/components/ui";

type Price = {
  code: string;
  label: string;
  duration_days: number;
  reference_price_vnd: number;
  effective_price_vnd: number;
  saving_vnd: number;
  discount_percent: number;
  revision: number;
  is_active: boolean;
  promotion: { label: string; ends_at: string } | null;
};
type Promotion = {
  code: string;
  price_code: string;
  label: string;
  sale_price_vnd: number;
  starts_at: string;
  ends_at: string;
  is_active: boolean;
  revision: number;
};
type Catalog = {
  offers: Price[];
  notice: string;
  market_references: {
    code: string;
    provider: string;
    product: string;
    price_vnd: number;
    duration_label: string;
    source_url: string;
    observed_on: string;
    note: string;
  }[];
  price_options: Price[];
  promotions: Promotion[];
};
const money = (value: number) =>
  new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  }).format(value);

export function VipPricing({ admin = false }: { admin?: boolean }) {
  const resource = useResource<Catalog>(
    admin ? "/admin/membership/prices" : "/membership/prices",
  );
  if (resource.loading) return <Loading />;
  if (resource.error || !resource.data)
    return <ErrorState message={resource.error} retry={resource.retry} />;
  const data = resource.data;
  return (
    <>
      {admin ? (
        <PageTitle
          title="Giá VIP và ưu đãi"
          description="Bảng giá tham khảo; có ngày hiệu lực, phiên bản và nhật ký thay đổi."
        />
      ) : (
        <h2>Tham khảo gói VIP cùng phụ huynh</h2>
      )}
      <div className="three-columns vip-prices">
        {data.offers.map((p) => (
          <section className="panel" key={p.code}>
            <span className="badge vip-badge">{p.label}</span>
            <h3>{money(p.effective_price_vnd)}</h3>
            <p>{p.duration_days} ngày cho một tài khoản học sinh</p>
            <p>Giá tham khảo đề xuất: {money(p.reference_price_vnd)}</p>
            {p.promotion && (
              <p className="notice success">
                {p.promotion.label}: giảm {money(p.saving_vnd)} (
                {p.discount_percent}%). Đến hết{" "}
                {new Date(
                  new Date(p.promotion.ends_at).getTime() - 1,
                ).toLocaleDateString("vi-VN", { timeZone: "Asia/Bangkok" })}
                .
              </p>
            )}
            <p>
              Toán, Tiếng Việt, Tiếng Anh và phần lớn AI Academy; bài nâng cao,
              gợi ý theo bước, lab mô phỏng và sản phẩm từ mẫu.
            </p>
          </section>
        ))}
      </div>
      <p className="notice">{data.notice}</p>
      <details className="panel">
        <summary>Tham khảo thị trường Việt Nam · khảo sát 12/10/2026</summary>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Đơn vị / sản phẩm</th>
                <th>Mốc giá</th>
                <th>Phạm vi</th>
              </tr>
            </thead>
            <tbody>
              {data.market_references.map((r) => (
                <tr key={r.code}>
                  <td>
                    <a href={r.source_url} target="_blank" rel="noreferrer">
                      {r.provider} · {r.product}
                    </a>
                  </td>
                  <td>
                    {money(r.price_vnd)} · {r.duration_label}
                  </td>
                  <td>{r.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p>
          Giá và điều kiện của từng đơn vị có thể thay đổi. VietTree là gói tự
          học; các gói có giáo viên trực tiếp có phạm vi khác.
        </p>
      </details>
      {admin && (
        <>
          <section className="panel">
            <h2>Chỉnh giá đề xuất</h2>
            {data.price_options.map((p) => (
              <PriceEditor
                key={p.code + ":" + p.revision}
                price={p}
                onSaved={resource.retry}
              />
            ))}
          </section>
          <PromotionEditor
            key={data.promotions.map((p) => p.code + p.revision).join(",")}
            data={data}
            onSaved={resource.retry}
          />
        </>
      )}
    </>
  );
}
function PriceEditor({
  price,
  onSaved,
}: {
  price: Price;
  onSaved: () => void;
}) {
  const [value, setValue] = useState(price.reference_price_vnd);
  const [password, setPassword] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");
  const [active, setActive] = useState(price.is_active);
  async function save() {
    try {
      await api(`/admin/membership/prices/${price.code}`, {
        method: "PUT",
        body: JSON.stringify({
          label: price.label,
          reference_price_vnd: value,
          is_active: active,
          revision: price.revision,
          actor_password: password,
          reason,
        }),
      });
      onSaved();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <details className="panel">
      <summary>
        {price.label} · {money(price.reference_price_vnd)}
      </summary>
      <label>
        Giá tham khảo (VND)
        <input
          aria-label={`Giá ${price.label}`}
          type="number"
          min={1000}
          max={10000000}
          value={value}
          onChange={(e) => setValue(Number(e.target.value))}
        />
      </label>
      <label>
        <input
          type="checkbox"
          checked={active}
          onChange={(e) => setActive(e.target.checked)}
        />{" "}
        Hiển thị gói giá
      </label>
      <label>
        Lý do thay đổi
        <input value={reason} onChange={(e) => setReason(e.target.value)} />
      </label>
      <label>
        Mật khẩu quản trị
        <input
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <button className="button secondary" onClick={() => void save()}>
        Lưu giá {price.label}
      </button>
      <p role="alert">{message}</p>
    </details>
  );
}
function PromotionEditor({
  data,
  onSaved,
}: {
  data: Catalog;
  onSaved: () => void;
}) {
  const [selected, setSelected] = useState("");
  const chosen = data.promotions.find((p) => p.code === selected);
  return (
    <section className="panel">
      <h2>Tạo hoặc điều chỉnh ưu đãi</h2>
      <label>
        Chọn ưu đãi
        <select
          aria-label="Chọn ưu đãi"
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
        >
          <option value="">Ưu đãi mới</option>
          {data.promotions.map((p) => (
            <option key={p.code} value={p.code}>
              {p.label} · {p.code}
            </option>
          ))}
        </select>
      </label>
      <PromotionForm
        key={selected}
        options={data.price_options}
        initial={chosen}
        onSaved={onSaved}
      />
    </section>
  );
}
function PromotionForm({
  options,
  initial,
  onSaved,
}: {
  options: Price[];
  initial?: Promotion;
  onSaved: () => void;
}) {
  const [code, setCode] = useState(initial?.code || "");
  const [price, setPrice] = useState(initial?.price_code || "vip-30");
  const [label, setLabel] = useState(initial?.label || "");
  const [sale, setSale] = useState(initial?.sale_price_vnd || 79000);
  const [start, setStart] = useState(
    initial?.starts_at?.slice(0, 10) || "2026-10-12",
  );
  const [end, setEnd] = useState(
    initial
      ? new Date(new Date(initial.ends_at).getTime() - 1).toLocaleDateString(
          "en-CA",
          { timeZone: "Asia/Bangkok" },
        )
      : "2026-11-12",
  );
  const [active, setActive] = useState(initial?.is_active ?? true);
  const [password, setPassword] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");
  async function save() {
    try {
      await api("/admin/membership/promotions", {
        method: "POST",
        body: JSON.stringify({
          code,
          price_code: price,
          label,
          sale_price_vnd: sale,
          starts_at: start + "T00:00:00+07:00",
          ends_at: end + "T23:59:59.999+07:00",
          is_active: active,
          revision: initial?.revision,
          actor_password: password,
          reason,
        }),
      });
      onSaved();
    } catch (e) {
      setMessage((e as Error).message);
    }
  }
  return (
    <>
      <label>
        Mã ưu đãi
        <input
          disabled={!!initial}
          maxLength={50}
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </label>
      <label>
        Gói áp dụng
        <select value={price} onChange={(e) => setPrice(e.target.value)}>
          {options.map((p) => (
            <option key={p.code} value={p.code}>
              {p.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Tên ưu đãi
        <input
          maxLength={120}
          value={label}
          onChange={(e) => setLabel(e.target.value)}
        />
      </label>
      <label>
        Giá ưu đãi (VND)
        <input
          type="number"
          min={1000}
          value={sale}
          onChange={(e) => setSale(Number(e.target.value))}
        />
      </label>
      <div className="two-columns">
        <label>
          Ngày bắt đầu
          <input
            type="date"
            value={start}
            onChange={(e) => setStart(e.target.value)}
          />
        </label>
        <label>
          Ngày kết thúc (giờ Việt Nam)
          <input
            type="date"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
          />
        </label>
      </div>
      <label>
        <input
          type="checkbox"
          checked={active}
          onChange={(e) => setActive(e.target.checked)}
        />{" "}
        Bật ưu đãi trong thời gian đã chọn
      </label>
      <label>
        Lý do
        <input value={reason} onChange={(e) => setReason(e.target.value)} />
      </label>
      <label>
        Mật khẩu xác nhận
        <input
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <button className="button secondary" onClick={() => void save()}>
        Lưu ưu đãi
      </button>
      <p role="alert">{message}</p>
    </>
  );
}
