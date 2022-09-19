#include <Arduino.h>
#include <Servo.h>

//Servos
//Servo body; //id 0, pin number 3, min 560, max 2330
//Servo shoulder; //id 1, pin number 9, min 750, max 2200
//Servo elbow; //id 2, pin number 10, min 550, max 2400
//Servo wrist; //id 3, pin number 6, min 950, 2400
//Servo gripper; //id 4, pin number 11, min 550, max 2150
//Servo head; //id 5, pin number 5, min 550, max 2340

Servo servo_vec[6];

//Init position of all servos
const int servo_pins[] = {3, 9, 10, 6, 11, 5};

const int pos_init[] = {1700, 1500, 2000, 2200, 1650, 1600}; //can be set to anything really, we'll have to set these to something that looks like a natural starting position.
int curr_pos[6]; //current position of all the servos

const int pos_min[] = {560, 750, 550, 950, 550, 550};
const int pos_max[] = {2330, 2200, 2400, 2400, 2150, 2340};

int servo_id;
int new_pos;


void move_servo(const int servo_id, const int new_pos) {
  if (new_pos <= pos_max[servo_id] && new_pos >= pos_min[servo_id]) {
    int diff, steps, now, CurrPwm, NewPwm, delta = 6;

    //current servo value
    now = curr_pos[servo_id];
    CurrPwm = now;
    NewPwm = new_pos;

    /* determine interation "diff" from old to new position */
    diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
    steps = abs(NewPwm - CurrPwm);
    delay(10);

    for (int i = 0; i < steps; i += delta) {
      now = now + delta*diff;
      servo_vec[servo_id].writeMicroseconds(now);
      delay(20);
    }
    curr_pos[servo_id] = now;
    delay(10);
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

String input_data;
char char_array[6];



void loop() {
  //delay(1000);

  
  while (!Serial.available()) {
    delay(50);
  }
    //input_data = Serial.readString().toInt();
  //}
  
  input_data = Serial.readString();

  /
  //Serial.print(input_data)
  /*input_data = Serial.readString().toInt();
  int data_vec[5]; //first element is servo_id, id 1-4 is new position.
  int data = input_data;
  for (int i = 4; i > -1; i--) {
      data_vec[i] = data%10;
      data /= 10;
  }
*/
  servo_id = (int) input_data[1] - 48; 
  new_pos = 1000 * (int) input_data[1] + 100 * (int) input_data[2] + 10 * (int) input_data[3] + 1 * (int) input_data[4];

  delay(200);

  Serial.print(servo_id);
  //Serial.print(servo_id);
  //delay(200);

  //Serial.print(new_pos);



  /*while(Serial.available() >= 2){
    servo_id = Serial.readString().toInt();
    new_pos = Serial.readString().toInt();
    
  }*/

  /*while (!Serial.available()) {
    servo_id = Serial.readString().toInt();
  }*/
  
  
  
  //servo_id = Serial.readString().toInt();
  

  //move_servo(servo_id, new_pos);
  
  delay(1000);

}

