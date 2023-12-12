# Bank-Market-Data

## Setup
To setup this repo run the following whilst in the `Bank-Market-Data` directory. 
The port is important as the Javascript will be querying that port.

```
conda create -n "demo" python=3.9
conda activate demo
pip install -r requirements.txt
pip install uvicorn
pip install python-multipart
uvicorn main:app --reload --port 8000
```

## Running
In the front end, just double click on the index which will take you to a browser where you can submit the data contained in the `example.csv` file.
This file is just one example from the validation data set the model was trained on, which I took out. 
However, it provides a simple showcase of the model's predictions.
Additionally, you can click on the explained link to see why the model made that prediction.
The idea here was that maybe we want to get closer to the teams that use our solutions so that we can get more feedback. However, most importantly, we can intuitively name the variables to allow the staff to come back and tell us what the model finds useful when it is incorrect and roughly for whom it gets things wrong. Domain knowledge is super necessary, so getting their feedback and making it cross-intelligible would be cool. 