#include <Arduino.h>
#include <Servo.h>

//Servos
//Servo body; //id 0, pin number 3, min 560, max 2330, 180 degrees
//Servo shoulder; //id 1, pin number 9, min 750, max 2200, 110 degrees
//Servo elbow; //id 2, pin number 10, min 550, max 2400, 90 degrees (max value is too high, should be around 1700. Low value is backwards, high value is forwards and up.)
//Servo wrist; //id 3, pin number 6, min 950, 2400, 160 degrees (180 degrees would be nice, maybe wrong values?)
//Servo gripper; //id 4, pin number 11, min 550, max 2150, 0-33 mm 550=33 mm 2150=0 mm.
//Servo head; //id 5, pin number 5, min 550, max 2340, 180 degrees

Servo servo_vec[6];

//Init position of all servos
const int servo_pins[] = {3, 9, 10, 6, 11, 5};

const int pos_init[] = {1445, 2200, 1150, 2400, 550, 1445}; //can be set to anything really, we'll have to set these to something that looks like a natural starting position.
int curr_pos[6]; //current position of all the servos

const int pos_min[] = {560, 750, 550, 950, 550, 550};
const int pos_max[] = {2330, 2200, 2400, 2400, 2150, 2340};

int servo_id;
int new_pos;
String input_data;
int input_data_int[5];


bool move_servo(const int servo_id, const int new_pos) {
  if (new_pos <= pos_max[servo_id] && new_pos >= pos_min[servo_id]) {
    int diff, steps, now, CurrPwm, NewPwm, delta = 6;

    //current servo value
    now = curr_pos[servo_id];
    CurrPwm = now;
    NewPwm = new_pos;

    /* determine interation "diff" from old to new position */
    diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
    steps = abs(NewPwm - CurrPwm);

    for (int i = 0; i < steps; i += delta) {
      now = now + delta*diff;
      servo_vec[servo_id].writeMicroseconds(now);
      delay(20);
    }
    curr_pos[servo_id] = now;
    return true;

  }
  else {
    Serial.print("Error: servo position not within required range");
    return false;
  }
}

void setup() {

  Serial.begin(57600); // Starts the serial communication


	//Attach each joint servo
	//and write each init position
  for (int i = 0; i < 6; i++) {
    servo_vec[i].attach(servo_pins[i]);
    servo_vec[i].writeMicroseconds(pos_init[i]);
  }

  //Initilize curr_pos vector
  byte i;
  for (i=0; i<(sizeof(pos_init)/sizeof(int)); i++){
    curr_pos[i] = pos_init[i];
  }

	delay(2000);
  Serial.print("Ready");
}

void loop() {
  //delay(1000);

  while (!Serial.available()) {
    delay(50);
  }
  
  input_data = Serial.readString();
  if (input_data == "99999") {
    Serial.print(99999);
  }
  else if (input_data.length() == 5) {
    Serial.print(input_data);

    for (int i = 0; i < 5; i++) {
      input_data_int[i] = (int) input_data[i] - 48;
    }
    servo_id = input_data_int[0];
    new_pos = 1000 * input_data_int[1] + 100 * input_data_int[2] + 10 * input_data_int[3] + 1 * input_data_int[4];

    move_servo(servo_id, new_pos);
    
  } else {
    input_data = "";
    Serial.print("Error: data was not 5 characters long");
  }
    delay(1000);

}

