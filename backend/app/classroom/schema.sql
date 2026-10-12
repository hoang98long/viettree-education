ALTER TABLE classes ADD COLUMN edit_revision INTEGER NOT NULL DEFAULT 1 CHECK(edit_revision > 0);
ALTER TABLE class_enrollments ADD COLUMN recognition_alias VARCHAR(40);
ALTER TABLE ai_lessons ADD COLUMN minimum_plan_code VARCHAR(20) NOT NULL DEFAULT 'vip' REFERENCES membership_plans(code);
UPDATE ai_lessons SET minimum_plan_code='free' WHERE code IN ('AI1-01','AI2-01','AI3-01','AI4-01','AI4-04','AI4-27','AI5-01');
INSERT INTO membership_plan_features(plan_code,feature_code) VALUES
 ('vip','academy.full'),('vip','academy.lab'),('vip','academy.studio') ON CONFLICT DO NOTHING;

CREATE TABLE classroom_settings (
 class_id UUID PRIMARY KEY REFERENCES classes(id) ON DELETE RESTRICT,
 recognition_enabled BOOLEAN NOT NULL DEFAULT TRUE,
 updated_by UUID REFERENCES users(id), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE learning_assignment_batches (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), actor_id UUID NOT NULL REFERENCES users(id),
 class_id UUID REFERENCES classes(id), kind VARCHAR(20) NOT NULL CHECK(kind IN ('assessment','lesson','ai_lesson')),
 resource_id UUID NOT NULL, idempotency_key UUID NOT NULL, fingerprint CHAR(64) NOT NULL,
 due_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(actor_id,idempotency_key)
);
CREATE TABLE learning_assignment_targets (
 batch_id UUID NOT NULL REFERENCES learning_assignment_batches(id),
 student_id UUID NOT NULL REFERENCES student_profiles(student_id),
 assignment_id UUID REFERENCES student_assignments(id), PRIMARY KEY(batch_id,student_id)
);
CREATE INDEX learning_assignment_targets_student ON learning_assignment_targets(student_id,batch_id);
CREATE TABLE class_award_batches (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(), class_id UUID NOT NULL REFERENCES classes(id),
 category VARCHAR(20) NOT NULL CHECK(category IN ('MATH','VIETNAMESE','ENGLISH','AI','AI_PROJECT')),
 period_start TIMESTAMPTZ NOT NULL, period_end TIMESTAMPTZ NOT NULL,
 resource_key VARCHAR(100) NOT NULL DEFAULT 'all', published_by UUID NOT NULL REFERENCES users(id),
 published_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), CHECK(period_end>period_start),
 UNIQUE(class_id,category,period_start,period_end,resource_key)
);
CREATE TABLE class_awards (
 batch_id UUID NOT NULL REFERENCES class_award_batches(id), rank SMALLINT NOT NULL CHECK(rank BETWEEN 1 AND 3),
 student_id UUID NOT NULL REFERENCES student_profiles(student_id), alias VARCHAR(40) NOT NULL,
 score NUMERIC(6,3) NOT NULL CHECK(score BETWEEN 0 AND 100), completed INTEGER NOT NULL CHECK(completed>0),
 PRIMARY KEY(batch_id,rank), UNIQUE(batch_id,student_id)
);
CREATE TABLE vip_price_options (
 code VARCHAR(40) PRIMARY KEY, label VARCHAR(100) NOT NULL,
 duration_days INTEGER NOT NULL CHECK(duration_days IN (30,90,365)),
 reference_price_vnd INTEGER NOT NULL CHECK(reference_price_vnd>0),
 is_active BOOLEAN NOT NULL DEFAULT TRUE, revision INTEGER NOT NULL DEFAULT 1,
 updated_by UUID REFERENCES users(id), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE vip_promotions (
 code VARCHAR(50) PRIMARY KEY, price_code VARCHAR(40) NOT NULL REFERENCES vip_price_options(code),
 label VARCHAR(120) NOT NULL, sale_price_vnd INTEGER NOT NULL CHECK(sale_price_vnd>0),
 starts_at TIMESTAMPTZ NOT NULL, ends_at TIMESTAMPTZ NOT NULL,
 is_active BOOLEAN NOT NULL DEFAULT TRUE, revision INTEGER NOT NULL DEFAULT 1,
 updated_by UUID REFERENCES users(id), CHECK(ends_at>starts_at)
);
CREATE TABLE vip_market_references (
 code VARCHAR(50) PRIMARY KEY, provider VARCHAR(80) NOT NULL, product VARCHAR(160) NOT NULL,
 price_vnd INTEGER NOT NULL CHECK(price_vnd>0), duration_label VARCHAR(80) NOT NULL,
 source_url TEXT NOT NULL CHECK(source_url LIKE 'https://%'), observed_on DATE NOT NULL,
 note TEXT NOT NULL
);
INSERT INTO vip_price_options(code,label,duration_days,reference_price_vnd) VALUES
 ('vip-30','VIP 30 ngày',30,99000),('vip-90','VIP 90 ngày',90,269000),('vip-365','VIP 365 ngày',365,899000);
INSERT INTO vip_promotions(code,price_code,label,sale_price_vnd,starts_at,ends_at) VALUES
 ('training-launch-30','vip-30','Ưu đãi trải nghiệm đào tạo',79000,'2026-10-12T00:00:00+07:00','2026-11-13T00:00:00+07:00'),
 ('training-launch-90','vip-90','Ưu đãi học đều đặn',219000,'2026-10-12T00:00:00+07:00','2026-11-13T00:00:00+07:00'),
 ('training-launch-365','vip-365','Ưu đãi đồng hành năm học',699000,'2026-10-12T00:00:00+07:00','2026-11-13T00:00:00+07:00');
INSERT INTO vip_market_references(code,provider,product,price_vnd,duration_label,source_url,observed_on,note) VALUES
 ('monkey-junior','Monkey','Monkey Junior',799000,'1 năm','https://monkey.edu.vn/dang-ky-hoc','2026-10-12','Giá ưu đãi hiển thị tại bảng giá công khai; sản phẩm tiếng Anh, không cùng phạm vi với VietTree.'),
 ('monkey-pro','Monkey','Combo Monkey Pro',1299000,'1 năm','https://monkey.edu.vn/dang-ky-hoc','2026-10-12','Giá ưu đãi hiển thị, gồm nhiều ứng dụng. Có thể có ưu đãi thanh toán riêng.'),
 ('olm-vip','OLM','VIP đa môn',1400000,'12 tháng','https://cdp.olm.vn/tin-tuc/Huong-dan-mua-tai-khoan-VIP-545093','2026-10-12','Mốc giá bài hướng dẫn công khai/indexed; checkout không truy cập được trong khảo sát, cần xác nhận lại với OLM.'),
 ('edupia-class','Edupia','AI Class và giáo viên quốc tế',220000,'Từ / tháng','https://hocbong.edupia.vn/hocbongai_2026','2026-10-12','Giá quảng bá từ 220.000đ/tháng, có điều kiện; gồm giáo viên, không so sánh ngang với gói tự học.');
