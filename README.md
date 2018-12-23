# Course Watch Utility Backend
# Marshall Peng Winter Break 2018

## About

It's sometimes really hard to get into popular classes at Dartmouth, given the small class sizes. One issue that many students face during add-drop period is that they don't know when other people drop the course, leaving an open spot. Normally, students would have to obsessively check the course timetable by hand for openings, so it pretty much comes down to luck whether or not you check at a time right when someone drops but before someone else takes it.

I wrote a script to fix this problem for myself a while back, but it after asking around, many of my friends said they would enjoy being able to use this service. So, I revamped an old project, serving the old script as a single page web-app that anyone can use.

To use it, all you have to do is fill out the form on the website, and wait for the email telling you that a slot has opened, then you go and register.

This repository contains the code for the backend portion of the Web app. Please take a look at the corresponding repo for the frontend, also on my Github page.

How it works is pretty simple.

1. User fills form, Frontend sends `POST` request to backend
2. Backend receives request and simply adds request to database after a few validation checks
3. Cronjob : ~20 minutes or so
	* read all requests from db
	* check each course request
		* if we find that slots are available
			* remove request from db and send email to user
			
Please, if you notice something or have suggestions, feel free to reach out to me. I'm always willing to make this better.

[Live Application](https://course-watch-utility-1d35d.firebaseapp.com)
			
## Screenshot

![](https://imgur.com/xNIqtMr.png)

## Tech Stack / Services Used

* Python 2.7
* Flask
* Firebase Auth
* Firebase Realtime Database
* Google App Engine
* SendGrid API (for emails)



## Installation/Development

Follow the directions [here](https://cloud.google.com/appengine/docs/standard/python/quickstart) in the "Before you Begin" section to make sure you have all the requirements for google app engine.


Install dependencies with `virtualenv`

```
virtualenv env
source env/bin/activate
pip install -t lib -r requirements.txt
```

Test the application with 

```
dev_appserver.py app.yaml
```

## License

This project is licensed under the MIT license - see [LICENSE.txt](LICENSE.txt) for details