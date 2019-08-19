**ST0324 Internet of Things CA2 Step-by-step Tutorial**

##### SCHOOL OF DIGITAL MEDIA AND INFOCOMM TECHNOLOGY (DMIT)

# IOT CA2 Gardening Water Dispenser

# Step-by-step Tutorial

ST 0324 Internet of Things (IOT)


## Table of Contents
```

* Section 1 Overview of Gardening Water Dispenser
* Section 2 Hardware requirements
* Section 3 Hardware setup
* Section 4 Create a “Thing”
* Section 5 DynamoDB Setup
* Section 6 AWS EC2 Hosting of Web Application
* Section 7 Reading RFID/NFC tags setup
* Section 8 Program setup
* Section 9 Web interface setup
* Section 10 Expected outcome
* Section 11 References

```
### Section 1 Overview of Gardening Water Dispenser

## A. What is Gardening Water Dispenser about?
The garden automatic watering tool, it activates whenever the soil moisture goes below the specific value,captures a picture at the same time prior to the environment, takes in light values as well as the temperature values around the plant, monitoring the plant as tight as possible, to ensure its survival.  Garden watering tool is for those who are keen on saving money and time. It is designed to ease the burdens of watering plants on a daily basis,  adjustment of the dripping volume at a given time which means the plants won’t be taking in insufficiently or excessively.

## B. How the final RPI set-up looks like
```
Final Set-up
```






```
Overview of the system
```

## C. How the web application looks like?


### Section 2 Hardware requirements 

#### Hardware checklist

Here are the hardware needed and what they are used for.



#### DHTT sensor
a) This DHT11 Temperature and Humidity Sensor features a calibrated digital signal output with the temperature and humidity sensor capability. This sensor includes a resistive element and a sensor for wet NTC temperature measuring devices. In this project, DHTT sensor 

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/DHT11.jpg "DHT11")

#### Light Dependant Resistor (LDR)
b)The resistance of a photoresistor decreases with increasing incident light intensity, in other words, it detects the amount of light value. In this project, the LDR plays a part in detecting the current light values.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/LDR.png "DHT11")

#### MCP3008 ADC
c) With MCP3008 you can read quite a few analog signals from the Pi.  This chip is a great option if you just need to read simple analog signals, like from a temperature or light sensor. This part plays a big role in reading values taken from the LDR/sensors.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/MCP3008.jpg "Optional Title")

#### Resistor (6 x 330 Ω Resistors, 3 x 10K Ω Resistor)
d)Resistor helps to ensure the flow tothe rasp berry pi is smooth and not be damaged.
![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")


#### Arduino
e) Arduino boards are actually micro-controllers rather than 'full' computers. Arduino lacks a full operating system but can run written code that is interpreted by its firmware. It is much flexible than the normal raspberry pi and can execute codes directly without no OS overhead.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/Arduino.jpg "Optional Title")



### Section 3 Hardware Setup

In this section, we will connect the neccessary parts displayed in section 2.

## Frizing Diagram



### Section 4 Create a "Thing"

#### Setting Up Your "Thing"
a) First, navigate to Iot Core

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")


b) Under manage, select things and choose register a thing.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")

c) Choose Create a single thing.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")

d) Enter a name for your project thing. Click next.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")

e) Click create certificate. Download all four files. As for the root CA, download the VeriSign Class 3 Public Primary G5 root CA certificate file.

![Alt text](https://github.com/999sky999/CA2_IOT/blob/master/GitHub%20Images/resistor.png "Optional Title")
