# Milestone 01 Release Note

วันที่ออก: 2026-02-17  
สถานะ: Released

## เป้าหมายที่ส่งมอบ
- ทำ V3 foundation ให้ใช้งานประจำวันได้จริงสำหรับการดูบทสนทนาแบบ near real-time
- สร้าง baseline ที่พร้อมต่อยอดสู่ analytics และ AI insight ใน Milestone 02

## สิ่งที่ส่งมอบใน M01
1. Core Runtime
- Ingestion watcher จากหลายผู้ใช้ (`poramet`, `support`, `first`)
- API server + Web dashboard บนพอร์ต `8020`
- สคริปต์ปฏิบัติการ: `start_v3.sh`, `stop_v3.sh`, `status_v3.sh`

2. Dashboard
- ดูรายการ sessions + messages
- กรองตาม owner
- auto-refresh เมื่อแท็บ active
- ดาวน์โหลดต่อ session เป็น `JSON`, `CSV`, `Markdown`

3. API Baseline
- `GET /api/health`
- `GET /api/sessions?owner=<owner>&limit=<n>`
- `GET /api/messages?session_id=<session_id>`
- มี input validation และ error format มาตรฐาน (`400`)

4. Documentation
- Architecture: `docs/ARCHITECTURE_V3.md`
- Milestone plan: `docs/MILESTONE_01_EXECUTION_PLAN.md`
- API reference: `docs/API_REFERENCE.md`
- Test report: `docs/MILESTONE_01_TEST_REPORT.md`

## ผลทดสอบ
- Smoke test ผ่านตามขอบเขต M01
- Health endpoint และ API หลักตอบกลับถูกต้อง
- Dashboard ใช้งานได้จริงกับข้อมูลหลาย owner

## Known Constraints
- ยังไม่มี role-based access ภายใน dashboard (จะทำใน M02)
- ยังไม่มี scheduled insight report อัตโนมัติ (จะทำใน M02)
- Monitoring/alerting เชิงระบบยังเป็นระดับพื้นฐาน

## แผนถัดไป (M02)
1. Structured tagging (`project`, `intent`, `status`)
2. Daily/weekly AI insight generation
3. Role-based access model และ retention policy
