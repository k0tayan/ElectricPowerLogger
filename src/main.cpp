#include <Arduino.h>

const float LOGIC_VOLTAGE = 5.f;
const float R_l = 1.f;         // 0.3 Ohm
const float CT_RATIO = 3000.f; // 3000:1
const float GAIN = 60.f;

const float MAX_CURRENT = LOGIC_VOLTAGE * CT_RATIO / (R_l * GAIN);

const float VOLTAGE = 100.f;

const size_t N = 30;
float data[N] = {0.0f};
float movingAverage(float *data, int n)
{
  float sum = 0;
  for (int i = 0; i < n; i++)
  {
    sum += data[i];
  }
  return sum / n;
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);

  for (size_t i = 0; i < N; i++)
  {
    data[i] = VOLTAGE * analogRead(A0) / 1024.0 * MAX_CURRENT;
  }
}

void loop()
{
  // put your main code here, to run repeatedly:
  float start = micros();

  float current = analogRead(A0) / 1024.0 * MAX_CURRENT;

  float electricPower = current * VOLTAGE;

  for (size_t i = 0; i < N - 1; i++)
  {
    data[i] = data[i + 1];
  }
  data[N - 1] = electricPower;
  float result = movingAverage(data, N);

  Serial.println(result);

  float end = micros();
  while (end - start < 1000)
  {
    end = micros();
  }
}