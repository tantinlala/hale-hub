#include <RCSwitch.h>

// Used for IR remote control of outlet
#include <RCSwitch.h>

// Parameters specific to RC outlets
#define SERIAL_COMMUNICATION_BAUD_RATE 9600
#define IR_PROTOCOL 1
#define IR_TRANSMITTER_PIN_NUMBER 5
#define IR_PULSE_LENGTH 180
#define CODE_TYPE 24

// 1 byte communication protocol
#define OUTLET_ID_BITS 0b00000110
#define OUTLET_STATE_BIT 0b00000001
#define VALID_COMMAND_SIGNATURE_BITS 0b11111000
#define VALID_COMMAND_SIGNATURE 0b10101000

// ASCII Cheat Sheet:
// ¨ - 168 - Turn outlet 0 off
// © - 169 - Turn outlet 0 on
// ª - 170 - Turn outlet 1 off
// « - 171 - Turn outlet 1 on
// ¬ - 172 - Turn outlet 2 off
// N/A - 173 - Turn outlet 2 on

typedef struct
{
  int offCommand;
  int onCommand;
} outletCommandCodeSet_t;

static const outletCommandCodeSet_t OUTLET_COMMAND_CODES[] =
{
  {.offCommand = 5574972, .onCommand = 5574963}, // outlet 0
  {.offCommand = 5575116, .onCommand = 5575107}, // outlet 1
  {.offCommand = 5575436, .onCommand = 5575427}, // outlet 2
};

// Used for IR remote control of outlet
RCSwitch g_outletSwitch = RCSwitch();
bool g_debugLedOn = false;

void setup(void)
{
  // Start serial communication so we can accept commands
  Serial.begin(SERIAL_COMMUNICATION_BAUD_RATE);
  
  // Set up IR transmitter
  g_outletSwitch.enableTransmit(IR_TRANSMITTER_PIN_NUMBER);
  g_outletSwitch.setProtocol(IR_PROTOCOL);
  g_outletSwitch.setPulseLength(IR_PULSE_LENGTH);

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void toggleDebugLed(void)
{
  if (g_debugLedOn)
  {
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    g_debugLedOn = false;
  }
  else
  {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    g_debugLedOn = true;
  }
}

void loop(void)
{
  if (millis() % 1000 == 0)
  {
    toggleDebugLed();
  }
  
  if (Serial.available() > 0)
  {
    uint8_t command = Serial.read();
    uint8_t commandSignature = (command & VALID_COMMAND_SIGNATURE_BITS);
    uint8_t outletID = (command & OUTLET_ID_BITS) >> 1;
    uint8_t onRequested =  (command & OUTLET_STATE_BIT);
    
    if ((commandSignature == VALID_COMMAND_SIGNATURE) &&
        (outletID < sizeof(OUTLET_COMMAND_CODES)/sizeof(OUTLET_COMMAND_CODES[0])))
    {
      if (onRequested)
      {
        g_outletSwitch.send(OUTLET_COMMAND_CODES[outletID].onCommand, CODE_TYPE);
      }
      else
      {
        g_outletSwitch.send(OUTLET_COMMAND_CODES[outletID].offCommand, CODE_TYPE);
      }
    }
  }
}
