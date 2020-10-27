# F1 Database Application

## Website Link:
https://f1stat-292509.uc.r.appspot.com/

## Team Members:
| Names: | EID: | GitHub Username: |
| -------| -----| -----------------|
| Kevin Medina | kom298 | kvnmedina | 
| Alan Zhang | adz343 | adz00 |
| Edie Zhou | ez3437 | edie-zhou |
| Samuel Yeboah | say438 | samuel-akwesi-yeboah | 

## Phase 1 Completion Times:
|   | Kevin Medina | Alan Zhang | Edie Zhou | Samuel Yeboah |   
| - | ------------ | ---------- | --------- | ------------- |
| Estimated | 4 hrs. | 5 hrs. | 2 hrs. | 3 hrs. |
| Actual | 4 hrs. | 5 hrs. | 5 hrs. | 3 hrs. |

## Phase 2 Completion Times:
|   | Kevin Medina | Alan Zhang | Edie Zhou | Samuel Yeboah |
| - | ------------ | ---------- | --------- | ------------- |
| Estimated | # hrs. | # hrs. | # hrs. | # hrs. |
| Actual | # hrs. | # hrs. | # hrs. | # hrs. |

## Environment Setup:
You will need a working version of Python 3 installed on your computer. Create the virtual environment using this command:

Linux: `python3 -m venv env`
Windows: `py -m venv env`

Once you have created the environment, activate the environment with this linux command:
`source env/bin/activate (you're on your own with windows :) )` 

With the environment active, install the dependencies from the `requirements.txt` file with this command:

`pip3 install -r requirements.txt`

## Deploying the Website Locally:
Before deploying the website, you will need to retrieve and unpack the `images.zip` archive in the 
`static/images` directory. `images.zip` contains all of our static images, and it is available from the
Google Drive of our shared `utairlab@gmail.com` account.
Use `source env/bin/activate` to activate the environment and run the app with `python3 app.py`

## Deploying the Website on Google Cloud:
You will need credentials for `utairlab@gmail.com`. Check the pinned post in the `#backend`  Slack channel for credentials.

You will need the `gcloud` binary, [click me for gcloud installation instructions](https://cloud.google.com/sdk/docs/install).

[Click me for instructions on deploying the webapp to google cloud](https://codelabs.developers.google.com/codelabs/cloud-app-engine-python3/#5).
