/*int motor1_pin1 =2; 
int motor1_pin2 =3;//3 high
int motor2_pin2 =4;//4 high
int motor2_pin1 =5;

int motor3_pin1 =6; 
int motor3_pin2 =7;//3 high
int motor4_pin2 =8;//4 high
int motor4_pin1 =9;

int motor5_pin1 =10; 
int motor5_pin2 =11;//3 high
int motor6_pin2 =12;//4 high
int motor6_pin1 =13;*/

int motorpin1[12] = {2, 4, 6, 8, 10, 12};
int motorpin2[12] = {3, 5, 7, 9, 11, 13};


int now[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
int sign[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
int goal[12] = {0,0,0,0,0,0,0,0,0,0,0,0};
char mode[5] = {'a','b','c','d','e'};

int t=2000;


void setup() {
  for(int i =0 ; i<12 ; i++){
    pinMode(motorpin1[i],OUTPUT);
    pinMode(motorpin2[i],OUTPUT);
  }
  Serial.begin(9600);
  while (!Serial) {} // toadd
  Serial.println("Serial Connected"); //toadd
  reset();
  // put your setup code here, to run once:

}

void loop() {
  char read_data;

 // Serial.print(mode[0]);
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    read_data = Serial.read();
    
    if(read_data == mode[0]){
      Serial.println("mode 0 ");
      goal[0] = 0; goal[1] = 0; goal[2] = 0; goal[3] = 0;
      goal[4] = 0; goal[5] = 0; goal[6] = 0; goal[7] = 0;
      goal[8] = 0; goal[9] = 0; goal[10] = 0; goal[11] = 0;
    }
    
    if(read_data == mode[1]){
      Serial.println("mode 1");
      goal[0] = 2; goal[1] = 2; goal[2] = 2; goal[3] = 2;
      goal[4] = 0; goal[5] = 0; goal[6] = 0; goal[7] = 0;
      goal[8] = 1; goal[9] = 1; goal[10] = 1; goal[11] = 1;
    }

    else if(read_data == mode[2]){
      Serial.println("mode 2 ");
      goal[0] = 3; goal[1] = 3; goal[2] = 3; goal[3] = 3;
      goal[4] = 1; goal[5] = 1; goal[6] = 1; goal[7] = 1;
      goal[8] = 2; goal[9] = 2; goal[10] = 2; goal[11] = 2;
    }

    else if(read_data == mode[3]){
      Serial.println("mode 3 ");
      goal[0] = 5; goal[1] = 5; goal[2] = 5; goal[3] = 5;
      goal[4] = 0; goal[5] = 0; goal[6] = 0; goal[7] = 0;
      goal[8] = 1; goal[9] = 1; goal[10] = 1; goal[11] = 1;
    }
    else if(read_data == mode[4]){
      Serial.println("mode 3 ");
      goal[0] = 0; goal[1] = 5; goal[2] = 5; goal[3] = 0;
      goal[4] = 0; goal[5] = 5; goal[6] = 5; goal[7] = 0;
      goal[8] = 0; goal[9] = 5; goal[10] = 5; goal[11] = 0;
    }

    /*
    else if(read_data == mode[4]){
      Serial.println("type your goal : ");
      for(int i =0 ; i<6 ; i++){
        goal[i] = Serial.parseInt();
      }

     if(goal[0] <0  ){
        reset();
     }
    }
    */
    

    

    
    int m = maximum();
    Serial.print("number of steps : ");
    Serial.println(m);
    for(int j = 0; j<m ; j++){

      
      Serial.println("goal :" );
      for(int i = 0; i< 12; i++){
        Serial.print(goal[i]);
        Serial.print(", ");
        if( i%4 == 3) Serial.println();
      }
      Serial.println();

      Serial.println("now :" );
      for(int i = 0; i< 12; i++){
        Serial.print(now[i]);
        Serial.print(", ");
        if( i%4 == 3) Serial.println();
      }
      Serial.println();
      
      sign_identifier();
      actuater();
      halt_everything();

   
    }
    Serial.println("-------Final Status-------- : ");
    Serial.println("goal :" );
    for(int i = 0; i< 12; i++){
      Serial.print(goal[i]);
      Serial.print(", "); 
      if( i%4 == 3) Serial.println();
    }
    Serial.println();

    Serial.println("now :" );
    for(int i = 0; i< 12; i++){
      Serial.print(now[i]);
      Serial.print(", ");  
      if( i%4 == 3) Serial.println();
    }
    Serial.println();
    
  }
  
}

void reset(){
  for(int i = 0; i<12; i++){
    sign[i] = -1;
  }
  motor();
  delay(5*t);
}


void actuater(){
  motor();
  delay(t);
}

int maximum(){
  int maximum = abs(goal[0] - now[0]);
  for(int i = 0; i<12-1; i++){
    if( abs(goal[i+1] -now[i+1])> maximum){
      maximum = abs(goal[i+1] -now[i+1]);
    }
    
  }

  return maximum;
}

void sign_identifier(){
  for(int i = 0; i <12; i++){
    if(goal[i]>now[i]){
      sign[i] = 1;
      now[i]++;
    }
    else if(goal[i]<now[i]){
      sign[i] = -1;
      now[i]--;
    }
    else if(goal[i] == now[i]){
      sign[i] = 0;
    }
  }
}

void motor(){
  for(int i =0; i<12; i++){
      if(sign[i]==1){
        digitalWrite(motorpin1[i],LOW);
        digitalWrite(motorpin2[i],HIGH);    
      }
      else if(sign[i]==-1){
        digitalWrite(motorpin1[i],HIGH);
        digitalWrite(motorpin2[i],LOW);   
      }
      else if(sign[i]==0){
        digitalWrite(motorpin1[i],LOW);
        digitalWrite(motorpin2[i],LOW); 
      }
  }
}


void halt_everything(){
  for(int i =0; i<12; i++){
    digitalWrite(motorpin1[i],LOW);
    digitalWrite(motorpin2[i],LOW);
    
  }
  
}

