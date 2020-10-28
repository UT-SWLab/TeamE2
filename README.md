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
| Story | Assignee | Estimated Time | Completion Time |
| ----- | -------- | -------------- | --------------- |
| As a user, I want to view a racer's win history, team, age, and all personal information. | Edie | 3 hrs. | 2 hrs. |
| As a user, I want to see some general information on each driver before clicking on their card so that I don't need to go all the way to their instance page. | Alan | 2 hrs. | 3 hrs. |
| As a user, I want a home page so that I can navigate between all of the various pages that are available. | Sam | 3 hrs. | 2 hrs. |
| As someone with poor eyesight, I want the user interface to be simple and easy to navigate. | Sam | 2 hrs. | 2 hrs. |
| As a user, I want to view a constructor's current and former team members, race statistics, and nationality. | Kevin | 4 hrs. | 5 hrs. |

## Phase 2 Completion Times:
| Story | Assignee | Estimated Time | Completion Time |
| ----- | -------- | -------------- | --------------- |
| As a user, I want to see the past teams that a driver has driven on so that I can see their career progression. | Alan | 2 hrs. | 4 hrs. |
| As a user, I want to see the number of wins for a constructor or a driver so that I can determine who is a better racer and what teams are the best. | Kevin | 4 hrs. | 5 hrs. |
| As a developer, I want pictures that accurately represent each instance. | Edie | 2 hrs. | 8 hrs. |
| As a developer, I want the ability to test my code so I know the software is free from bugs before I push to production. | Sam | 4 hrs. | 4 hrs. |
| As a developer, I want to be able to test my UI so that I know it is bug free before I push to production. | Alan | 2 hrs. | 2 hrs. | 
| As a user, I want to view the web application's data sources and method of retrieval. This is for my own verification and assurance. | Sam | 3 hrs. | 3 hrs. |
| As a user, I want the webpages to load quickly and responsively, while still providing a breadth of information. | Kevin | 1 hr. | 3 hrs. |
| As a user, I want to navigate through the model instances using an intuitive feature. | Alan | 3 hrs. | 4 hrs. |
| As a user, I want see the fastest laps of all time on a circuit to see what kind of speed the drivers are able to accomplish. | Kevin | 2 hrs. | 2 hrs. |


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
