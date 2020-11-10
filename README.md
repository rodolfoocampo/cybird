## CyBird

### A smart house for selective feeding of native species and bird monitoring. 

To run the project, you will need: 

- Raspberry Pi 3
- Edge TPU
- Servo Motor
- A food dispenser mechanism that can be controlled by a servo
- A house. Our model has used the model found here: https://coral.ai/projects/bird-feeder/#recommended-electronics

You will need to configure the Edge TPU following these steps: https://coral.ai/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime

You will need to set up the tensorflowlite runtime, following these steps: https://coral.ai/docs/accelerator/get-started/#2-install-the-tensorflow-lite-library

We are using a different code than the one provided in the bird house tutorial. Our extensions have: 

Included control of a servo
Upload the data to a Google Sheet
The Google Sheet can feed a dashboard like the one shown here: https://datastudio.google.com/u/0/reporting/ddfa43c1-f1eb-4a55-895f-63411924b9e3/page/SrtnB
Gets information from Weather and Air Quality to aid research for understanding their effects on birds

To run the code, follow the steps above, clone this repo, and run: 

```
python3 classify_image.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels models/inat_bird_labels.txt

```
