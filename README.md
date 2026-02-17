# TCI-GLTP

Team Conversation Intelligence สำหรับ GLTP

## วัตถุประสงค์
TCI-GLTP ใช้สำหรับรวบรวมบทสนทนาใน Codex session จากผู้ใช้หลายคน แปลงเป็นข้อมูลเชิงโครงสร้าง และรองรับทั้ง:
- Operational viewer (near real-time) สำหรับติดตามงานประจำวัน
- Analytics base สำหรับต่อยอด AI insight

## ขอบเขตปัจจุบัน (V3 Foundation)
- Multi-user session ingestion จาก `.codex/sessions`
- SQLite schema (`sessions`, `messages`)
- API endpoints สำหรับดึง sessions/messages
- Web dashboard สำหรับดู timeline/เนื้อหาการสนทนา และดาวน์โหลด `JSON/CSV/Markdown` ต่อ session
- Background watcher สำหรับอัปเดตข้อมูลอัตโนมัติ

## โครงสร้าง Repository
- `src/tci_gltp/` โค้ดหลักของระบบ
- `web/` หน้า dashboard
- `scripts/start_v3.sh` เริ่ม ingest watcher + API/web
- `scripts/stop_v3.sh` หยุด background services
- `scripts/status_v3.sh` ตรวจสถานะ runtime
- `data/processed/tci_gltp.sqlite3` ฐานข้อมูล analytics
- `docs/` เอกสาร architecture และ milestone

## ข้อกำหนดก่อนใช้งาน
- Python 3.10+
- มี ACL ที่อนุญาตให้อ่าน source session roots ได้ครบ
- สภาพแวดล้อม Linux (scripts ปัจจุบันเป็น bash)

## แหล่ง Session ที่ตั้งค่าไว้
กำหนดใน `src/tci_gltp/config.py`:
- `/home/poramet/.codex/sessions`
- `/home/support/.codex/sessions`
- `/home/first/.codex/sessions`

## วิธีรันระบบ
```bash
cd /workspace/TCI-GLTP
./scripts/start_v3.sh
```

เปิด dashboard:
- `http://127.0.0.1:8020/`
- `http://192.168.1.88:8020/`

## วิธีหยุดระบบ
```bash
./scripts/stop_v3.sh
```

## วิธีตรวจสถานะ
```bash
./scripts/status_v3.sh
```

## API
- `GET /api/health`
- `GET /api/sessions?owner=<owner>&limit=<n>`
- `GET /api/messages?session_id=<session_id>`

## หมายเหตุด้านข้อมูล
- เวลาใน source เป็น UTC (`Z`)
- เวลาแสดงผลถูกแปลงเป็น Asia/Bangkok (`+07`)
- Ingestion เป็นแบบ idempotent (`messages` ใช้ deterministic `message_id`)

## แผน Milestone
- แผนดำเนินงาน: `docs/MILESTONE_01_EXECUTION_PLAN.md`
- API reference: `docs/API_REFERENCE.md`
- รายงานทดสอบ: `docs/MILESTONE_01_TEST_REPORT.md`
- Release note: `docs/MILESTONE_01_RELEASE_NOTE.md`
