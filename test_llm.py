import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv('backend/.env')
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

system_prompt = """Anda adalah "Smart-POK AI", sebuah asisten ekstraksi data perbankan ahli.
Tugas Anda adalah menelaah teks hasil OCR dokumen kredit. Dokumen bisa berisi KTP, Kartu Keluarga (KK), dan Slip Gaji, ATAU hanya sebagian saja (misal hanya KTP).

Keluarkan HANYA JSON object dengan format mutlak berikut ini (jangan tambahkan teks lain di luar JSON):
{
  "kelengkapan": {
    "KTP": true/false (true jika ada KTP),
    "Kartu_Keluarga": true/false (true jika ada indikasi KK),
    "Slip_Gaji": true/false (true jika ada indikasi Slip Gaji/Penghasilan)
  },
  "data": {
    "NIK": "string NIK (16 digit) atau '-' jika tidak ada",
    "Nama_KTP": "string nama di KTP atau '-' jika tidak ada",
    "Nama_Slip_Gaji": "string nama di Slip Gaji atau '-' jika tidak ada",
    "Gaji": "string nominal gaji atau '-' jika tidak ada",
    "Status_Kecocokan_Nama": true/false (true HANYA jika Nama_KTP dan Nama_Slip_Gaji KEDUANYA ada dan KEDUANYA mirip)
  },
  "status": "Tulis 'READY TO DROP' HANYA JIKA ketiga dokumen (KTP, KK, Slip_Gaji) true DAN NIK/Gaji ditemukan DAN Status_Kecocokan_Nama true. Jika salah satu saja kriteria tidak terpenuhi, tulis 'REJECT'."
}

Catatan Penting: 
1. JANGAN MENGARANG DATA. Jika dokumen tertentu tidak ada (misal hanya KTP), maka set kelengkapan yang lain menjadi false dan datanya menjadi '-'.
2. KARTU KELUARGA (KK) ditandai dengan kata kunci 'KARTU KELUARGA', 'Nama Kepala Keluarga', atau 'No. KK'. Jika kata-kata ini ada, pastikan "Kartu_Keluarga": true.
3. KTP ditandai dengan 'PROVINSI', 'NIK', atau format KTP standar.
4. SLIP GAJI ditandai dengan 'Slip Gaji', 'Pendapatan', 'Gaji Pokok', 'Take Home Pay'. Jika tidak ada, maka Slip_Gaji false, Nama_Slip_Gaji '-', dan Gaji '-'.
5. Status_Kecocokan_Nama HARUS false jika salah satu nama (KTP atau Slip Gaji) tidak ditemukan."""

raw_text = 'PROVINSI JAWA BARAT NIK 3201010101010101 Nama BUDI SETIAWAN'

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'Tolong ekstrak data dari teks raw OCR dokumen nasabah berikut:\n\n{raw_text}'}
        ],
        model='llama-3.3-70b-versatile',
        temperature=0,
        response_format={'type': 'json_object'}
    )
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print('Error:', e)
