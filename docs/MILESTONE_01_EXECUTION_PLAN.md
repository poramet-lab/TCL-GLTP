# แผนดำเนินงาน Milestone 01

## Objective
ทำให้ V3 foundation เสถียรพอสำหรับใช้งานประจำวัน เพื่อดูสถานะการสนทนาแบบ live และค้นประวัติได้อย่างเชื่อถือได้

## สถานะปัจจุบัน (อัปเดตล่าสุด: 2026-02-17)
- เสร็จแล้ว:
- Ingestion watcher + API server + dashboard ใช้งานได้
- มีสคริปต์ `start_v3.sh`, `stop_v3.sh`, `status_v3.sh`
- Dashboard รองรับ owner filter, session/message view และ auto-refresh (active tab)
- รองรับการดาวน์โหลดต่อ session: `JSON`, `CSV`, `Markdown`
- API hardening สำหรับ query params และรูปแบบ error `400` มาตรฐานเสร็จแล้ว
- เอกสาร `API Reference` และ `Smoke Test Report` เสร็จแล้ว
- เอกสารหลักปรับเป็นภาษาไทยเรียบร้อย
- ค้างดำเนินการ:
- ปิดเอกสาร release note ของ M01 และเริ่มแผน M02

## In Scope
1. ความเสถียรของ Ingestion สำหรับผู้ใช้ทุกคนที่ตั้งค่าไว้
2. ความน่าเชื่อถือของ API และรูปแบบ response ที่สม่ำเสมอ
3. การใช้งาน Dashboard ให้ลื่นในงานประจำวัน
4. Operational scripts สำหรับ start/stop/status
5. Governance baseline (ACL และ data handling)

## Work Packages
1. Data Ingestion
- ตรวจว่า source roots อ่านได้ครบ
- เพิ่มตัวเลข ingestion counters ใน logs (sessions/messages)
- ยืนยันว่า re-run แล้วไม่เกิดข้อมูลซ้ำ

2. API Contract
- ยืนยันพฤติกรรม endpoint และ default limits
- เพิ่ม error response แบบเบาสำหรับ invalid params
- จัดทำตัวอย่าง response สำหรับอ้างอิง

3. Dashboard
- ให้ owner filter และการเปิด session/message ทำงานเร็ว
- คง periodic refresh เมื่อแท็บ active
- ตรวจให้ใช้งานบนหน้าจอมือถือได้โดยไม่พัง

4. Operations
- start script ต้องเปิด watcher + API server ได้ครบ
- stop script ต้องหยุดทั้งสอง process อย่างสะอาด
- status script ต้องรายงาน PID, port, health endpoint

5. Governance Baseline
- ตรวจ ACL read access ครบทุก user เป้าหมาย
- ไม่แก้ไฟล์ raw source โดยตรง
- ระบุที่เก็บ logs/DB ให้ตรวจสอบย้อนหลังได้

## Definition of Done
- `./scripts/start_v3.sh` เริ่มระบบได้สำเร็จ
- `./scripts/status_v3.sh` รายงานสถานะ healthy
- Dashboard เปิดได้และดูอย่างน้อย 1 session ต่อ owner ได้
- `GET /api/health` ตอบ `{ "ok": true }`
- `GET /api/sessions` และ `GET /api/messages` ตอบ JSON ถูกต้อง

## Definition of Done (Checklist)
- [x] Start/Stop/Status scripts ใช้งานได้
- [x] Dashboard ใช้งานได้จริงจากข้อมูลหลาย owner
- [x] Health endpoint ใช้งานได้
- [x] ดาวน์โหลด `JSON/CSV/Markdown` ได้จากหน้า dashboard
- [x] API input validation ครบตามที่ตกลง
- [x] เอกสาร API examples พร้อมสำหรับทีมใช้งาน
- [x] Smoke test รอบสุดท้ายผ่านและบันทึกผล

## M1 UI Gap Closure (ต้องปิดก่อนขึ้น M2)
### Scope Freeze (M1)
- ไม่เพิ่มฟีเจอร์ใหม่จนกว่าจะปิด UI gap ที่ค้าง
- โฟกัสเฉพาะความครบถ้วน, ความชัดเจน, และความเสถียรของ UI เดิม

### UI Gap List (จัดลำดับความสำคัญ)
1. Critical (ต้องเสร็จก่อน)
- ปุ่ม/ฟอร์มหลักใช้งานไม่ได้ หรือพาไปหน้าผิด
- state สำคัญไม่ครบจนเกิดการใช้งานผิด เช่น ไม่มี `loading`, `error`, `empty`
- บันทึกสำเร็จไม่ชัดเจน ทำให้ผู้ใช้กดซ้ำหรือคิดว่าข้อมูลหาย

2. Important (ควรเสร็จในรอบเดียวกัน)
- label/screen title ไม่สื่อความหมาย
- ลำดับการใช้งานสับสน ต้องกดหลายขั้นเกินจำเป็น
- mobile layout ใช้งานได้แต่มีจุดติดขัด (scroll/spacing/tap area)

3. Polish (ทำเมื่อ 2 ระดับแรกผ่าน)
- spacing/alignment/consistency ของ component
- รูปแบบปุ่ม/สี/สถานะ ไม่สม่ำเสมอทั้งระบบ

### UI Definition of Done (M1)
- ทุกหน้าที่ใช้งานจริงมี state ครบ: `loading`, `empty`, `error`, `success`
- ฟอร์มหลักมี validation ครบ และแสดงข้อความผิดพลาดที่เข้าใจได้
- ปุ่มบันทึกมีสถานะ `disabled/processing` ระหว่างบันทึก
- หลังบันทึกมีผลลัพธ์ที่ยืนยันได้ชัดเจน (success toast/message)
- ไม่มี UI blocker ระดับ Critical ค้าง
- รองรับการใช้งานบน desktop และ mobile ตาม flow หลักที่ตกลง

### Go/No-Go Gate ก่อนเริ่ม M2
- [ ] Critical UI gaps = 0
- [ ] Important UI gaps ปิดอย่างน้อย 90%
- [ ] ผ่าน UAT สั้น 1 รอบ (happy path + error path)
- [ ] อัปเดตหลักฐานใน `MILESTONE_01_TEST_REPORT.md`
- [ ] Owner อนุมัติ baseline M1 อย่างเป็นทางการ

## Risks
- ACL เปลี่ยนจนเห็นข้อมูลไม่ครบ
- ไฟล์ session ขนาดใหญ่ทำให้ ingestion ช้าลง
- process ถูกปิดโดยไม่มี monitoring

## Mitigation
- ใช้ status script เป็น routine check
- ทำ manual verification เป็นระยะจนกว่าจะมี monitoring
- เพิ่ม alerting/cron supervision ใน Milestone 02

## Next Milestone Preview (M02)
- Structured tagging pipeline (`project`, `intent`, `status`)
- Daily/weekly AI insight generation
- Role-based access model และ retention policy

## งานถัดไป (ลำดับแนะนำ)
1. ปิด Milestone 01
- สร้าง release note สั้นสำหรับทีมใช้งานจริง
- ยืนยัน baseline ที่อนุมัติแล้ว (API + Dashboard + Download)
2. เริ่ม Milestone 02
- ออกแบบ structured tagging (`project`, `intent`, `status`)
- ออกแบบ daily/weekly AI insight report
- กำหนด role-based access และ retention policy
