## CyBird

### A smart house for selective feeding of native species and bird monitoring. 

To run the project, you will need: 

- Raspberry Pi 3
- Edge TPU
- Servo Motor
- A food dispenser mechanism that can be controlled by a servo
- A house. Our model has used the model found here: https://coral.ai/projects/bird-feeder/#recommended-electronics

### Steps 

1. Configure your Raspberry Pi. We recommend using Python 3.5.

2. Configure the Edge TPU following these steps: https://coral.ai/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime

3. Set up the tensorflowlite runtime, following [these steps]https://coral.ai/docs/accelerator/get-started/#2-install-the-tensorflow-lite-library

4. Create a google sheet. Grab the Google Sheet Id. https://docs.google.com/spreadsheets/d/{youwillfindtheidhere}

5. Create four sheets in your Google Sheet. Don't change their names. In the Sheet4, in the A2 cell, write the name of the bird you want to feed as found in the models/nat_bird_labels.txt

6. If you want a dashboard, you can copy our original one here: https://datastudio.google.com/u/0/reporting/ddfa43c1-f1eb-4a55-895f-63411924b9e3/page/SrtnB and just set your Google Sheet as a Data Source. Or you can create your own, fed with the Google Sheet you made. 

### Selective feeding and monitoring

This project is based on the smart bird feeder created by the Coral team, found here: https://coral.ai/projects/bird-feeder/#how-it-works

Our project extends it in several ways.

The original Coral design just scares unintended birds with a noise from a speaker. This can be annoying for human users, ineffective and traumatizing for birds. Instead, we control a feeding mechanism that only opens when the intended bird is found. 

We upload all of the data to a user owned Google Sheet, and provide a dashboard. 


We are using a different code than the one provided in the bird house tutorial. Our extensions have: 



Included control of a servo
Upload the data to a Google Sheet
The Google Sheet can feed a dashboard like the one shown here: https://datastudio.google.com/u/0/reporting/ddfa43c1-f1eb-4a55-895f-63411924b9e3/page/SrtnB
Gets information from Weather and Air Quality to aid research for understanding their effects on birds

To run the code, follow the steps above, clone this repo, and run: 

```
python3 classify_image.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels models/inat_bird_labels.txt
```


