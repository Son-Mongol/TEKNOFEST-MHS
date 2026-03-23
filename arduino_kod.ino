// BU ARDUINO KODUDUR - SADECE ARDUINO'YA YÜKLENİR
void setup() {
  Serial.begin(9600); // Python ile aynı hızda konuşacaklar
}

void loop() {
  // Sensör verilerini okuduğunu varsayalım (Örnek rastgele sayılar)
  float voltaj = analogRead(A0) * (5.0 / 1023.0); 
  float guc = voltaj * 10.0;

  // Python'un beklediği format: voltaj,guc
  Serial.print(voltaj, 2); 
  Serial.print(",");      
  Serial.println(guc, 2); 

  delay(1000); // 1 saniye bekle
}
