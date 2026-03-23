/*
  TEKNOFEST MHS - Mikrobiyal Yakıt Hücresi Veri İzleme Sistemi
  Bu kod Arduino'ya yüklenmelidir.
*/

// --- AYARLAR ---
const int sensorPin = A0;    // MYH'nin (+) ucu A0'a, (-) ucu GND'ye
const float direnc = 1000.0; // Devreye bağladığınız direnç değeri (Ohm). Örn: 1000 (1k)

// Değişkenler
int sensorDegeri = 0;
float voltaj = 0.0;
float akim = 0.0;
float guc_watt = 0.0;
float guc_uW = 0.0;

void setup() {
    Serial.begin(9600); // Bilgisayar ile haberleşmeyi başlat (Python ile aynı hız)

    // Arduino Uno için 1.1V iç referansı kullanıyoruz (Daha hassas ölçüm için)
    // NOT: Eğer voltajınız 1.1V'dan yüksekse bu satırı silin!
    analogReference(INTERNAL); 
}

void loop() {
    // 1. Sensörden veriyi oku (0-1023 arası değer gelir)
    sensorDegeri = analogRead(sensorPin);

    // 2. Voltajı hesapla (1.1V referansına göre)
    // Eğer analogReference(INTERNAL) kullanıyorsak 1.1 ile çarpılır
    voltaj = sensorDegeri * (1.1 / 1023.0);

    // 3. Akımı hesapla (I = V / R) -> Amper cinsinden
    akim = voltaj / direnc;

    // 4. Gücü hesapla (P = V * I) -> Watt cinsinden
    guc_watt = voltaj * akim;

    // 5. Gücü mikroWatt (uW) cinsine çevir (Daha büyük sayılar için)
    guc_uW = guc_watt * 1000000.0;

    // 6. Verileri Seri Port üzerinden gönder 
    // Format: Voltaj,Güç (Python bu formatı bekliyor)
    Serial.print(voltaj, 4); // Virgülden sonra 4 basamak
    Serial.print(",");      // Araya virgül koyduk
    Serial.println(guc_uW, 4); // Gücü gönder ve yeni satıra geç

    delay(1000); // Her 1 saniyede bir ölçüm al
}
