import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  Calculator,
  Globe,
  ShieldCheck,
  Sprout,
} from "lucide-react";
import { Brand, TreeArt } from "@/components/ui";
export default function Landing() {
  return (
    <>
      <header className="public-header">
        <Brand />
        <nav>
          <a href="#subjects">Môn học</a>
          <a href="#approach">Cách học</a>
          <Link className="button small" href="/login">
            Đăng nhập <ArrowRight size={17} />
          </Link>
        </nav>
      </header>
      <main id="main" className="landing">
        <section className="hero">
          <div>
            <span className="eyebrow">
              <Sprout size={17} /> DÀNH CHO NHỮNG MẦM NON TRI THỨC
            </span>
            <h1>
              Mỗi điều em học,
              <br />
              một nhành cây <em>lớn lên.</em>
            </h1>
            <p>
              Khám phá kiến thức, luyện tập từng bước và tìm thấy niềm vui học
              mỗi ngày. VietTree đồng hành cùng em trên hành trình trưởng thành.
            </p>
            <Link className="button" href="/login">
              Vào góc học tập <ArrowRight size={19} />
            </Link>
            <span className="hero-note">
              <ShieldCheck size={18} /> Không quảng cáo · Không gian riêng tư
            </span>
          </div>
          <TreeArt />
        </section>
        <section id="subjects">
          <div className="section-heading">
            <div>
              <span className="eyebrow">HÀNH TRÌNH LỚP 4</span>
              <h2>Ba môn học, bao điều thú vị</h2>
            </div>
            <span className="pill">Lớp 1–5 · Lớp 4 đã sẵn sàng</span>
          </div>
          <div className="subject-grid">
            {[
              [
                "Toán",
                "Tìm quy luật, hiểu con số và giải bài toán quanh em.",
                Calculator,
                "math",
              ],
              [
                "Tiếng Việt",
                "Đọc để hiểu, chọn từ hay và viết điều em nghĩ.",
                BookOpen,
                "vietnamese",
              ],
              [
                "Tiếng Anh",
                "Hello! Khám phá từ mới và câu chuyện mỗi ngày.",
                Globe,
                "english",
              ],
            ].map(([title, description, Icon, color]) => {
              const I = Icon as typeof Calculator;
              return (
                <article
                  className={`subject-card ${color}`}
                  key={String(title)}
                >
                  <span className="subject-icon">
                    <I size={28} />
                  </span>
                  <h3>{String(title)}</h3>
                  <p>{String(description)}</p>
                  <Link href="/login" className="card-link">
                    Cùng khám phá <ArrowRight size={17} />
                  </Link>
                </article>
              );
            })}
          </div>
        </section>
        <section id="approach" className="approach">
          <span className="eyebrow">NHẸ NHÀNG, THEO NHỊP CỦA EM</span>
          <h2>
            Một chút hôm nay.
            <br />
            Vững vàng hơn ngày mai.
          </h2>
          <div className="three-columns">
            {[
              [
                "01",
                "Hiểu bài thật rõ",
                "Bài học ngắn gọn, ví dụ gần gũi và phần ghi nhớ dễ hiểu.",
              ],
              [
                "02",
                "Thử sức từng bước",
                "Lưu câu trả lời, xem lại và nhận lời giải sau khi nộp.",
              ],
              [
                "03",
                "Ôn đúng điều cần",
                "Gợi ý luyện tập dựa trên kết quả của em, với lý do rõ ràng.",
              ],
            ].map(([n, t, d]) => (
              <article key={n}>
                <span className="step-number">{n}</span>
                <h3>{t}</h3>
                <p>{d}</p>
              </article>
            ))}
          </div>
        </section>
      </main>
      <footer className="public-footer">
        <Brand />
        <span>Học điều hay, lớn mỗi ngày.</span>
        <Link href="/login">Đăng nhập</Link>
      </footer>
    </>
  );
}
