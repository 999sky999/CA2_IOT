**ST0324 Internet of Things CA2 Step-by-step Tutorial**

##### SCHOOL OF DIGITAL MEDIA AND INFOCOMM TECHNOLOGY (DMIT)

# IOT CA2 Gardening Water Dispenser

# Step-by-step Tutorial

ST 0324 Internet of Things (IOT)


## Table of Contents


- Section 1 Overview of Gardening Water Dispenser
- Section 2 Hardware requirements
- Section 3 Hardware setup
- Section 4 Create a “Thing”
- Section 5 DynamoDB Setup
- Section 6 AWS EC2 Hosting of Web Application
- Section 7 Reading RFID/NFC tags setup
- Section 8 Program setup
- Section 9 Web interface setup
- Section 10 Expected outcome
- Section 11 References

### Section 1 Overview of Gardening Water Dispenser

## A. What is Gardening Water Dispenser about?
The garden automatic watering tool, it activates whenever the soil moisture goes below the specific value,captures a picture at the same time prior to the environment, takes in light values as well as the temperature values around the plant, monitoring the plant as tight as possible, to ensure its survival.  Garden watering tool is for those who are keen on saving money and time. It is designed to ease the burdens of watering plants on a daily basis,  adjustment of the dripping volume at a given time which means the plants won’t be taking in insufficiently or excessively. Users can also access the website to control the machine on/off switch manually by both mobile or computer.

## B. How the final RPI set-up looks like
```
Final Set-up
```






```
Overview of the system
```

## C. How the web application looks like?

### Main Page
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/application(1).jpg "DHT11")

### Second Page
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Application(2).jpg "DHT11")

### Third Page
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Application(3).jpg "DHT11")

### Fourth Page
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Application(4).jpg "DHT11")


### Section 2 Hardware requirements 

#### Hardware checklist

Here are the hardware needed and what they are used for.



#### DHTT sensor
a) This DHT11 Temperature and Humidity Sensor features a calibrated digital signal output with the temperature and humidity sensor capability. This sensor includes a resistive element and a sensor for wet NTC temperature measuring devices. In this project, DHTT sensor will sense the surrounding temperature and display it in the website as real time value.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/DHT11.jpg "DHT11")

#### Light Dependant Resistor (LDR)
b)The resistance of a photoresistor decreases with increasing incident light intensity, in other words, it detects the amount of light value. In this project, the LDR plays a part in detecting the current light values and displaying it in the website as real time value.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/LDR.png "DHT11")

#### MCP3008 ADC
c) With MCP3008 you can read quite a few analog signals from the Pi.  This chip is a great option if you just need to read simple analog signals, like from a temperature or light sensor. This part plays a big role in reading values taken from the LDR/sensors.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/MCP3008.jpg "Optional Title")

#### Arduino
d) Arduino boards are actually micro-controllers rather than 'full' computers. Arduino lacks a full operating system but can run written code that is interpreted by its firmware. It is much flexible than the normal raspberry pi and can execute codes directly without no OS overhead.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Arduino.jpg "Optional Title")

#### Soil Moisture Sensor
e) Soil Moisture Sensor/ for this project, that requires for automatic plant supply, the moisture of the soil must be measured, the soil Moisture Sensor must be included. 

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/moisture.jpg "Optional Title")

#### RPI camera
f)The RPI camera is attached to the RPI ribbon, which will be used to capture images on the environment.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/picamera.jpg "DHT11")

#### LCD screen
g) Takes in data from sensors and displaying it in the physical screen.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/LCD.jpg "DHT11")

#### Resistor (6 x 330 Ω Resistors, 3 x 10K Ω Resistor)
a)2 Resistor helps to ensure the flow tothe rasp berry pi is smooth and not be damaged.
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")

b) As this application requires a Light Dependent Resistor, we will use a 10K ohms Resistor to help moderate the flow of current.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor2.jpg "Optional Title")



### Section 3 Hardware Setup

In this section, we will connect the neccessary parts displayed in section 2.

## Frizing Diagram
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/diagram1.JPG "Optional Title")

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/diagram2.JPG "Optional Title")



### Section 4 Create a "Thing"

#### Setting Up Your "Thing"
a) First, navigate to Iot Core

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20155802.png "Optional Title")

b) Click 'Secure', then 'Policies' Click 'Create' in the top right corner.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20162247.png)

c) Give the policy a name.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20162541.png)

d) Scroll down to 'Add statements'. Click 'Advanced mode', and a text box should appear.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20162756.png)

e) Replace the contents of the text box with the following:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}

```
f) Click 'Create'.

g) Return to 'Iot Core'. Under manage, select things, then click the 'Create' button in the top right corner.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20160104.png "Optional Title")

h) Click 'Create a single thing'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20160453.png "Optional Title")

i) Give your thing a name, then scroll to the bottom of the page and click 'Next'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20160740.png "Optional Title")

j) Click create certificate.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20161042.png "Optional Title")

k) Download all certificates shown on the page. Note that the last download link opens a page in a new tab. Download the 'Amazon Root CA 1' certificate. Save them to a secure and easily accessible location as you will need them later in order for your Raspberry Pis and server to connect to AWS IoT's MQTT broker. After all certificates have been downloaded, click 'Activate'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20161337.png)

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20161749.png)

l) On the next page, attach the policy you created earlier to your thing, then click 'Register thing'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20163335.png)

### Section 5 Create IAM roles

a) Click 'Services' at the top of the page. Look for 'IAM' under 'Security, Identity and Compliance', and click on it.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20164327.png)

b) Select 'Roles', then click 'Create role'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20164550.png)

c) On the next page, under 'Choose service to use role', select 'IoT'. Under 'Select your use case', select 'IoT', then click 'Next: Permissions'.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20164756.png)

d) Click 'Next: Tags' without doing anything. On the next page, click 'Next: Review' without doing anything. On the last page, name the role 'aws_iot_mqtt_rules', then click 'Create role'.

e) Return to IAM roles. Click on 'aws_iot_mqtt_rules', then click 'Attach policies'. Find the following policy, and attach it to the role.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20171115.png)

f) Repeat steps (a) and (b) under this section. Under 'Choose service to use role', select 'EC2'. Click 'Next: Permissions'. Use the search bar to find the following roles and attach them.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20171530.png)

g) Click 'Next: Tags', then 'Next: Review'. Name the role as 'ec2_server'. Click 'Create role'

h) Return to IAM Roles. Click 'Create role', then select 'Lambda' under 'Choose service to use this role'. Click 'Next: Permissions'. Attach the following policies:

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Annotation%202019-08-21%20172534.png)

i) Click 'Next: Tags', then 'Next: Review'. Name the role as 'updated_prefs_alerter'. Click 'Create role'

### Section 11 References

1) Practical 6
2) Practical 4

