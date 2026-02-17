# สถาปัตยกรรม V3 (ฉบับร่าง)

## Layers
1. Ingest: parse ไฟล์ jsonl sessions จากหลายผู้ใช้
2. Normalize: map ข้อมูลเข้าสู่ canonical records
3. Store: เก็บทั้ง raw และ analytics tables
4. Serve: ให้บริการ dashboard/API/search
5. Insight: สรุปผลแบบ schedule เพื่อช่วยวิเคราะห์

## Security
- ใช้ ACL-based access สำหรับ session roots
- ทำ PII masking ก่อนนำข้อมูลไปใช้งาน analytics
- ควบคุมสิทธิ์แบบ role-based viewer access
