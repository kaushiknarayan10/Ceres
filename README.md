# Ceres Imaging Take Home

## Goals
Given a s3 Bucket, the app gives the user the option to
- Get a list of all files available
- Download a specific file (pulling files directly from s3 using the boto3 library)
- For a specific file, show associated metadata
- Download all files in a zip

## Running
- Clone the directory to your local.
- Run `pip install -r requirements.txt`
- Run `python Home.py` and go to [127.0.0.1:5000](http://127.0.0.1:5000)
- If you have a different runtime of python, use `python3 Home.py`

## Information
It is recommended that you set up your own AWS CLI configuration. But if you do not have, there is an aws.config file that is used by the code.
The steps to comment/uncomment the relevant piece of code is in `Home.py`.
