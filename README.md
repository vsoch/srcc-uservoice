# UserVoice SRCC

This is the start of functions to work with UserVoice for Stanford Research Computing. Note that their default SDK has a bug that does not correctly add parameters to the GET request, and so it isn't possible to specify anything in particular. I have submit a [PR to fix this](https://github.com/uservoice/uservoice-python/pull/12), and in the meantime [my fork branch](https://github.com/vsoch/uservoice-python/tree/add/requests-get-params) will work for these functions.

      pip install -r requirements.txt


## API Authentication
You should [create an API token](https://developer.uservoice.com/docs/api/getting-started/) and create a file called `.secrets` in the present working directory, with the api key on the first line, and the api token on the second. Make sure you click the box that says "Trusted" for it to work. Then (since this is pretty rough) you can run [run.py](run.py) to get and save the tickets. I'd recommend running in ipython (terminal) so you have the tickets loaded and ready to go! Otherwise, just load them.

