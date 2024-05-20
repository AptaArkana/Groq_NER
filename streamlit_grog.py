import os
from dotenv import load_dotenv
import argparse
from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

client = Groq(
    api_key=groq_api_key
)

SYSTEM_PROMPT = "Anda adalah sistem Named Entity Recognition (NER) yang cerdas dan cerdas yang akan memberikan Output dalam format JSON. Saya akan memberi Anda definisi entitas yang perlu Anda ekstrak dan kalimat dari mana Anda perlu mengekstrak entitas dan hasilnya dalam format tertentu dengan contoh"

USER_PROMPT_1 = "Apakah Anda sudah jelas mengenai peran Anda?"

ASSISTANT_PROMPT_1 = "Tentu, saya siap membantu Anda dengan tugas NER Anda. Harap berikan saya informasi yang diperlukan untuk memulai."

PROMPT = (
    "Definisi Entitas :\n"
    "1. CRD : Entitas ini mengacu pada bilangan yang menunjukkan kuantitas atau jumlah. Sepeti satu, dua, lima ratus\n"
    "2. DAT: Entitas ini mengacu pada tanggal tertentu. Format tanggal bisa juga dalam bahasa alami. Seperti senin, selasa, atau 17-08-1945\n"
    "3. EVT : Entitas ini mengacu pada suatu kejadian atau peristiwa yang signifikan. Contoh: Olimpiade, Pemilu 2024, Perang Dunia III\n"
    "4. FAC : Entitas ini mengacu pada bangunan atau tempat yang digunakan untuk tujuan tertentu. Contoh: rumah sakit, sekolah, stadion.\n"
    "5. GPE : Entitas ini mengacu pada nama negara, kota, atau wilayah politik lainnya. Contoh: Indonesia, Jakarta, Amerika Serikat.\n"
    "6. LAW : Entitas ini mengacu pada undang-undang atau peraturan hukum. Contoh: Undang-Undang Dasar 1945, Peraturan Pemerintah No. 23 Tahun 2022.\n"
    "7. LOC : Entitas ini mengacu pada lokasi atau tempat geografis yang tidak termasuk dalam kategori GPE. Contoh: Gunung Everest, Laut Jawa, Sungai Nil.\n"
    "8. MON : Entitas ini mengacu pada jumlah uang atau mata uang. Contoh: Rp 1.000.000, USD 100, Yen 5.000.\n"
    "9. NOR : Entitas ini mengacu pada organisasi politik atau kelompok politik. Contoh: Partai Demokrat, Partai Golkar, Komisi Pemilihan Umum.\n"
    "10. ORD : Entitas ini mengacu pada bilangan urutan atau posisi dalam suatu deretan. Contoh: pertama, kedua, ketiga.\n"
    "11. ORG : Entitas ini mengacu pada organisasi atau lembaga selain yang bersifat politik. Contoh: Google, Perserikatan Bangsa-Bangsa (PBB), Universitas Harvard.\n"
    "12. PER : Entitas ini mengacu pada individu atau orang. Contoh: Joko Widodo, Nelson Mandela, Albert Einstein.\n"
    "13. PRC : Entitas ini mengacu pada persentase atau perbandingan dalam bentuk persen. Contoh: 50%, 75%, 100%.\n"
    "14. PRD : Entitas ini mengacu pada produk atau barang. Contoh: iPhone, Toyota Camry, Laptop Dell.\n"
    "15. QTY : Entitas ini mengacu pada jumlah atau kuantitas dari sesuatu. Contoh: dua lusin, tiga kilogram, sepuluh liter.\n"
    "16. REG : Entitas ini mengacu pada agama atau keyakinan spiritual. Contoh: Islam, Kristen, Hindu.\n"
    "17. TIM : Entitas ini mengacu pada waktu tertentu dalam sehari. Contoh: pukul 07.00, siang, malam.\n"
    "18. WOA : Entitas ini mengacu pada karya seni atau karya sastra. Contoh: Mona Lisa, War and Peace, Starry Night.\n"
    "18. LAN : Entitas ini mengacu pada bahasa yang digunakan dalam komunikasi. Contoh: Bahasa Indonesia, Bahasa Inggris, Bahasa Mandarin.\n"
    "\n"
    
    "Output Format:\n"
    "{{'CRD': [daftar entitas yang ada], 'DAT': [daftar entitas yang ada], 'EVT': [daftar entitas yang ada], 'FAC': [daftar entitas yang ada], 'GPE': [daftar entitas yang ada], 'LAW': [daftar entitas yang ada], 'LOC': [daftar entitas yang ada], 'MON': [daftar entitas yang ada], 'NOR': [daftar entitas yang ada], 'ORD': [daftar entitas yang ada], 'ORG': [daftar entitas yang ada], 'PER': [daftar entitas yang ada], 'PRC': [daftar entitas yang ada], 'PRD': [daftar entitas yang ada], 'QTY': [daftar entitas yang ada], 'REG': [daftar entitas yang ada], 'TIM': [daftar entitas yang ada], 'WOA': [daftar entitas yang ada], 'LAN': [daftar entitas yang ada]}}\n"
    "Langsung berikan Output dengan format yang telah diberikan, tidak usah ada kata kata seperti\n"
    "Examples: \n"
    "Berikut adalah hasil analisis NER\n"
    "Here is the output in the specified format:\n" 
    "ataupun sejenisnya\n"
    "Jika tidak ditemukan entitas maka tidak perlu ditampilkan\n"
    "Tidak boleh ada 2 value didalam satu entitas jika ada buat baru\n"
    "Examples: \n"
    "Output : 'GPE': ['Banten', 'Provinsi Banten', 'Kota Serang'] maka buat jadi 'GPE': ['Banten'],'GPE': ['Provinsi Banten'], 'GPE': ['Kota Serang']\n"
    "\n"
    "Examples:\n"
    "\n"
    "1. Sentence: Presiden Jokowi widodo bertemu dengan Perdana Menteri India untuk membahas pertemuan G20 di Bali, pada tanggal 20 September 2023.\n"
    "Output: {{'DAT': ['20 September 2023'], 'EVT':['G20'], 'GPE':['India'] 'GPE': ['Bali'], 'NOR': ['Presiden'], 'NOR': ['Perdana Menteri'], 'PER': ['Jokowi widodo']}}\n"
    "\n"
    "2. Sentence: John dan Sunita Roy adalah teman dan mereka bertemu satu sama lain pada 24/03/1998 di Samsung saat mereka menjadi rekan kerja.\n"
    "Output: {{'DAT': ['24/03/1998'],  'ORG':['Samsung'], 'PER': ['John'], 'PER': ['Sunita Roy']}}\n"
)

role = SYSTEM_PROMPT + '\n' + PROMPT

def chat_completion_response(final_prompt):
    response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": USER_PROMPT_1},
                    {"role": "assistant", "content": ASSISTANT_PROMPT_1},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0
            )
    return response.choices[0].message.content

def main():
    st.title("Named Entity Recognition (NER) System")

    user_input = st.text_area("Masukkan kalimat untuk diproses:")

    if st.button("Proses"):
        result = chat_completion_response(user_input)
        st.markdown(result)

if __name__ == "__main__":
    main()