import serial
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# --- AYARLAR ---
arduino_port = 'COM4'  # Kendi portuna göre değiştirmeyi unutma (Örn: COM3, COM5)
baud_rate = 9600

# Verileri saklamak için listeler
zaman_listesi = []
voltaj_listesi = []
guc_listesi = []

# Konsol çıktısını sadeleştirmek için son değerleri tutan değişkenler
son_voltaj = 0.0
son_guc = 0.0
veri_sayaci = 0  # Konsol çıktısını seyreltecek sayaç

# Grafik penceresini hazırla
try:
    plt.style.use('seaborn-darkgrid')
except:
    plt.style.use('ggplot')  # Eğer seaborn yoksa bunu kullanır

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.suptitle('TEKNOFEST MHS: Canlı Veri Analizi')

# Arduino bağlantısını başlat
try:
    ser = serial.Serial(arduino_port, baud_rate)
    print(f"{arduino_port} portuna bağlanıldı. Veri bekleniyor...")
    time.sleep(2)
except serial.SerialException:
    print(f"HATA: {arduino_port} portuna bağlanılamadı!")
    print("Lütfen Arduino kablosunu ve port ayarını kontrol edin.")
    raise SystemExit

# CSV dosyasını oluştur ve başlıkları yaz
dosya_adi = "myh_verileri_yeni.csv"
with open(dosya_adi, 'w', newline='') as f:
    yazici = csv.writer(f)
    yazici.writerow(["Tarih_Saat", "Voltaj (V)", "Guc (uW)"])

def animate(i):
    global son_voltaj, son_guc, veri_sayaci
    try:
        if ser.in_waiting > 0:
            arduino_data = ser.readline().decode('utf-8').strip()

            if arduino_data:
                veriler = arduino_data.split(',')

                if len(veriler) == 2:
                    voltaj = float(veriler[0])
                    guc = float(veriler[1])
                    su_an = datetime.now().strftime('%H:%M:%S')
                    veri_sayaci += 1

                    # Listelere ekle
                    zaman_listesi.append(su_an)
                    voltaj_listesi.append(voltaj)
                    guc_listesi.append(guc)

                    # Son 20 veriyi göster
                    gosterilecek_zaman = zaman_listesi[-20:]
                    gosterilecek_voltaj = voltaj_listesi[-20:]
                    gosterilecek_guc = guc_listesi[-20:]

                    # --- KONSOL ÇIKTISI DÜZENLEMESİ ---
                    if voltaj != son_voltaj or guc != son_guc or (veri_sayaci % 30) == 0:
                        print(f"{su_an} | V: {voltaj:.4f} V, P: {guc:.4f} uW")
                        son_voltaj = voltaj
                        son_guc = guc

                    # Dosyaya kaydet
                    with open(dosya_adi, 'a', newline='') as f:
                        yazici = csv.writer(f)
                        yazici.writerow([su_an, voltaj, guc])

                    # 1. Grafiği Çiz (Voltaj)
                    ax1.cla()
                    ax1.plot(gosterilecek_zaman, gosterilecek_voltaj, color='blue', label='Voltaj (V)', marker='o')
                    ax1.legend(loc='upper left')
                    ax1.set_ylabel('Gerilim (Volt)')
                    ax1.grid(True)

                    if gosterilecek_voltaj:
                        ax1.set_ylim(min(gosterilecek_voltaj) * 0.99, max(gosterilecek_voltaj) * 1.01)

                    # 2. Grafiği Çiz (Güç)
                    ax2.cla()
                    ax2.plot(gosterilecek_zaman, gosterilecek_guc, color='red', label='Güç (uW)', marker='o')
                    ax2.legend(loc='upper left')
                    ax2.set_ylabel('Güç (mikroWatt)')
                    ax2.set_xlabel('Zaman')
                    ax2.grid(True)

                    if gosterilecek_guc:
                        ax2.set_ylim(min(gosterilecek_guc) * 0.99, max(gosterilecek_guc) * 1.01)

                    plt.xticks(rotation=45)

    except ValueError:
        pass
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Animasyonu başlat
ani = FuncAnimation(fig, animate, interval=1000)

plt.tight_layout()
plt.show()

# Program kapatılırken portu serbest bırak
try:
    ser.close()
    print("Port kapatıldı.")
except:
    pass
