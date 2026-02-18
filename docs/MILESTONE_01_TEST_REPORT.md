# Milestone 01 Test Report

วันที่ทดสอบ: 2026-02-17 13:09:43 +0700
สภาพแวดล้อม: `/workspace/TCI-GLTP`

## Test Steps and Results
1. Start services
- Command: `./scripts/start_v3.sh`
- Result: PASS

2. Runtime status
- Command: `./scripts/status_v3.sh`
- Result: PASS (ingest/server running, port `8020` listening, health ok)

3. Health endpoint
- Command: `curl -s http://127.0.0.1:8020/api/health`
- Result: PASS
- Response: `{"ok": true}`

4. Sessions endpoint (valid)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?limit=2'`
- Result: PASS
- Response: JSON array with session objects

5. Sessions endpoint (invalid limit)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?limit=abc'`
- Result: PASS
- Response:
```json
{"error":{"code":"INVALID_LIMIT","message":"limit must be a positive integer (1-500)"}}
```

6. Sessions endpoint (invalid owner)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?owner=unknown'`
- Result: PASS
- Response:
```json
{"error":{"code":"INVALID_OWNER","message":"owner must be one of: first, poramet, support"}}
```

7. Messages endpoint (missing session_id)
- Command: `curl -s 'http://127.0.0.1:8020/api/messages'`
- Result: PASS
- Response:
```json
{"error":{"code":"MISSING_SESSION_ID","message":"session_id is required"}}
```

## Summary
- Smoke test ผ่านตามขอบเขต M01
- API validation และ error format มาตรฐานทำงานถูกต้อง

## UI/UX Feedback Consolidation (User-Centric)
อัปเดตล่าสุด: 2026-02-17

### Must (ต้องทำก่อนขึ้น M2)
1. เพิ่มช่องค้นหาข้อความด้านบนรายการ พร้อมแสดงผลลัพธ์เป็นรายการ session ที่พบ
2. ฝั่งซ้ายต้องแสดงสถานะรายการที่ถูกเลือกให้ชัดเจน (พื้นหลัง/เส้นเน้น/ตัวอักษรเด่น)
3. เมื่อเลือก session จากฝั่งซ้าย ฝั่งขวาต้องแสดงข้อความของ session นั้นทันทีและชัดเจน
4. ฝั่งขวาต้อง highlight คำค้นที่พบ และบอกตำแหน่งผลลัพธ์ (เช่น ลำดับที่พบ)
5. ย่อข้อมูลฝั่งซ้ายให้เน้นเฉพาะ owner + ช่วงเวลา + จำนวนข้อความ และลดความเด่นของชื่อไฟล์ยาว
6. ปรับการแสดงผลข้อความฝั่งขวาให้อ่านง่าย: รองรับ paragraph/bullet/code block และมี spacing ระหว่าง message
7. ทุกหน้าที่เกี่ยวข้องต้องมี state ครบ: loading, empty, error, success

### Should (ควรทำในรอบเดียวกันถ้าทัน)
1. เพิ่มปุ่มไปผลลัพธ์คำค้นถัดไป/ก่อนหน้าในฝั่งขวา
2. เพิ่ม sticky header ฝั่งขวาเพื่อบอกว่ากำลังดู session ใดอยู่
3. เพิ่มปุ่ม `Jump to latest` ใน panel ข้อความ
4. เพิ่มปุ่ม `Copy message` รายข้อความ
5. จัดรูปแบบ timestamp ให้เป็นมาตรฐานเดียวกันทั้งระบบ
6. ใช้ skeleton loading เพื่อลดความรู้สึกว่าระบบค้าง

### Later (เลื่อนไป M2 ได้)
1. Advanced search (query ซับซ้อน/regex/ฟิลเตอร์หลายชั้น)
2. ส่วนแสดงผลเชิง analytics ที่ไม่เกี่ยวกับ flow ค้นหาโดยตรง
3. การปรับ visual polish เชิงความสวยงามที่ไม่กระทบการใช้งานหลัก

## UAT Checklist (M1 UI Closure)
- [ ] ค้นหาคำแล้วเห็นรายการ session ที่พบในฝั่งซ้าย
- [ ] เลือกผลลัพธ์จากฝั่งซ้ายแล้วฝั่งขวาเปลี่ยนตามทันที
- [ ] ผู้ใช้แยกออกทันทีว่า session ไหนถูกเลือกอยู่
- [ ] คำค้นถูก highlight ชัดเจนในฝั่งขวา
- [ ] ข้อความยาวอ่านง่าย (มี paragraph/list spacing ชัด)
- [ ] กรณีไม่พบผลลัพธ์ มีข้อความแจ้งที่เข้าใจง่าย
- [ ] กรณีโหลดช้า ผู้ใช้เห็นสถานะ loading
- [ ] กรณีโหลดผิดพลาด ผู้ใช้เห็นข้อความ error ที่อ่านรู้เรื่อง

## Post-Implementation Verification (UI Search + Readability)
วันที่ทดสอบ: 2026-02-17 15:10:38 +0700

1. Search endpoint (valid query)
- Command: `curl -s 'http://127.0.0.1:8020/api/search_messages?q=AI&limit=3'`
- Result: PASS
- Notes: ได้รายการ session พร้อม `hit_count`

2. Search endpoint (missing query)
- Command: `curl -s 'http://127.0.0.1:8020/api/search_messages'`
- Result: PASS
- Response:
```json
{"error": {"code": "MISSING_QUERY", "message": "q is required"}}
```

3. Search endpoint (invalid owner)
- Command: `curl -s 'http://127.0.0.1:8020/api/search_messages?q=test&owner=unknown'`
- Result: PASS
- Response:
```json
{"error": {"code": "INVALID_OWNER", "message": "owner must be one of: first, poramet, support"}}
```

4. Frontend syntax guard (dashboard script)
- Command: `awk '/<script>/{flag=1;next}/<\\/script>/{flag=0}flag' web/index.html > /tmp/tci_gltp_dashboard.js && node --check /tmp/tci_gltp_dashboard.js`
- Result: PASS

5. Runtime health after deploy
- Command: `./scripts/status_v3.sh`
- Result: PASS (ingest/server running, port `8020` listening, health ok)
