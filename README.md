## CyBird

### A smart house for selective feeding of native species and bird monitoring. 

This bird house uses a mechanical bird feeder connected to an AI-enabled camera that detects and classifies birds, and feeds only selected species. It also records observations and provides an interactive data dashboard of bird visits. 

The project was created as a part of the [3Ai](https://3ainstitute.org/) masters program at the Australian National University, and is an extension of the Smart Bird Feeder by Google Coral. At [3Ai](https://3ainstitute.org/) we study how to develop safe, sustainable and responsible AI-enabled cyberphysical systems, and this we built this project as a way to explore those questions within the environmental cyberphysical systems space. 

The aim of the system to bring humans closer to wildlife in their backyard and gather data on urban bird populations by engaging people on citizen science.

To replicate this project, you will need:

- Raspberry Pi 3
- Edge TPU
- Servo Motor
- A food dispenser mechanism that can be controlled by a servo
- A bird house. Our model has used the model found [here](https://coral.ai/projects/bird-feeder/#recommended-electronics)

### Steps to build your own 

#### Software

1. Configure your Raspberry Pi. We recommend using Python 3.5.

2. Configure the Edge TPU following [these steps](https://coral.ai/docs/accelerator/get-started/#1-install-the-edge-tpu-runtime)

3. Set up the tensorflowlite runtime, following [these steps](https://coral.ai/docs/accelerator/get-started/#2-install-the-tensorflow-lite-library)


#### Mechanical Components

1. Connect your servo to pin 17 in the Raspberry Pi.
2. Attach your servo to the opening operator of the feeding mechanism. The servo will open less than 30 degrees. This can be adjusted changing the duty cycle found in classify_image.py

#### Selective feeding and monitoring

1. Create a google sheet. 

2. Grab the Google Sheet Id. It is found after the d in sheet link https://docs.google.com/spreadsheets/d/{youwillfindtheidhere}. 

Add this id in the read_selected_bird() function found in classify_image.py

```
def read_selected_bird(service):
  result = service.spreadsheets().values().get(
    spreadsheetId='id_goes_here', range='Sheet4!A2').execute()
  rows = result.get('values', [])
  name = rows[0][0]
  return name
 ```

3. Create four sheets in your Google Sheet. Don't change their names. In the Sheet4, in the A2 cell, write the name of the bird you want to feed as found in the models/nat_bird_labels.txt

4. Enable the Google Sheets API. Download the pickle and credentials.json files.

4. If you want a dashboard, you can copy our original one [here](https://datastudio.google.com/u/0/reporting/ddfa43c1-f1eb-4a55-895f-63411924b9e3/page/SrtnB) and just set your Google Sheet as a Data Source. Or you can create your own, fed with the Google Sheet you made. 

#### Running the code

Once you have done the above, clone this repo, and run: 

```
python3 classify_image.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels models/inat_bird_labels.txt
```

This will start taking a photo every second. It will record an observation in your Google Sheet. 

### Inspiration for the project 

This project is based on the smart bird feeder created by the Coral team, [found here](https://coral.ai/projects/bird-feeder/#how-it-works)

Our project extends it in several ways.

- The original Coral design just scares unintended birds with a noise from a speaker. This can be annoying for human users, ineffective and traumatizing for birds. Instead, we control a feeding mechanism that only opens when the intended bird is found. 

- We upload all of the data to a user owned Google Sheet, and provide a dashboard. 

- We use a Raspberry Pi instead of a Coral. 

### Other use cases

This system can be used by conservation and research teams to enable AI enabled bird monitoring. The model can also be changed for identifying other animals, and enabled selective feeding of vulnerable species. To do this, you can find more models [here](https://coral.ai/models/), or train your own, and just the --model parameter.
