# Shopository

This project is for the 2022 Shopify Developer Intern Challenge to build an image repository. The word repository made me think of a git repository, so I built mine with a similar structure. I built an API using Flask in Python and a CLI to abstract the API requests. 

## Features
I added five main commands: Push, Pull, Rename, Remove, and LS. 
 - Push takes a local image on your computer and uploads it to the repository
 - Pull takes an image on the repository and downloads it to your computer
 - Rename allows you to change the name of an image on the repository
 - Remove permanently deletes an image from the repository
 - LS lists each image in the repository
 
## Description of Implementation
I have it setup to store the images in a really simple way. It simply takes each pushed image and stores it in an `images/` directory with file name of the format `{image_id}{imagefile}`. For example, a file at index 1 with name "koopa.jpg" would be stored at `images/01koopa.jpg`. This way, it's possible to have duplicate image names, which can be clarified by the image id. For simplicity, because this is a small scale application, I put a cap of 100 total images allowed to be uploaded. I did not add any organizational structure, so any more than this would make it difficult to use. Again, for simplicity and small scale, I didn't integrate a database. Instead, each time the server is started, it reads in each of the images in the `images/` directory, and stores them in a simple dictionary of the form `{index: imagefile}`. This was an easy way to get persistence. 

I check to make sure it is a valid image file simply by checking the extension to see if it is one of `png, jpg, jpeg, gif, pdf`. Although this doesn't guarantee it's an actual picture file, for a general user, this will do the trick. 

I created three API endpoints:
 - `/images` and `/images/<image_id>` which is used to push, pull, rename, and remove images
 - `/images/getname` which serves as a helper API call to tell the CLI what the name of the image at `<image_id>` is
 - `/images/ls`, which serves the LS command
 
I creatively named my CLI "Shopository". This has the main purpose of abstracting away the API calls from the user and replacing them with simple, easy-to-use commands. I used the click module as a base for an easier CLI implementation. 

## Usage
### Installation for local usage
 - In a terminal, `git clone https://github.com/OwenMatsuda/shopify-challenge.git`
 - `cd shopify-challenge`
 - If you want to use a virtual environment, now is the time to set it up
   - If you don't already have virtualenv installed, `pip install virtualenv`
   - `python -m virtualenv venv`
   - `source venv/bin/activate`
 - Then install the requirements `pip install -r requirements.txt`
 - Open up a second terminal window and activate your virtual environment if you have one `source venv/bin/activate`
 - In this second terminal, start up the server `python3 app.py`
 - Back in your first terminal, you can now start performing `./Shopository` commands
 
The following commands are provided:
 - `./Shopository ls`
 - `./Shopository push IMAGE_FILE`
 - `./Shopository pull IMAGE_ID`
   - Optional `-o, --output` that allows you to specify the download location
   - By default, it downloads into the current directory with the same name as the file on the repository
 - `./Shopository remove IMAGE_ID`
   - Prompts user to confirm they want to permanently delete the file, can be overriden by adding `--yes` to the command
 - `./Shopository rename IMAGE_ID NAME`
 
### Example
Let's say we have an image file in my current directory called "goomba.png" that we want to upload into the repository. We can do this by simply typing `./Shopository push "goomba.png"`. 

Now we can see it in the repository by typing `./Shopository ls`. Note that it says the corresponding index for "goomba.png" is 0. 

Let's now say that we want to change the name of this file on the repository to "roomba.png". To do this, we would type `./Shopository rename 0 "roomba.png"`, where 0 is the corresponding index that is attached to "goomba.png". Now if we type `./Shopository ls`, we see that the image name changed to "roomba.png".

Now let's say that we wanted a new copy of "roomba.png" on our local computer. To do this, we would type `./Shopository pull 0`, again where 0 is the corresponding index that is attached to "roomba.png". If we look in our local directory, we can now see a copy of "roomba.png".

Finally, let's say that we no longer want a copy of "roomba.png" on the repository. We can delete this by typing `./Shopository remove 0`, where 0 is the index belonging to "roomba.png". This will permanently delete our file, so if we're sure, we can type `y` to confirm. Now if we type `./Shopository ls`, we can see that it's empty, meaning that our file no longer exists.


## Testing
I approached testing in a simple manner using unit tests to make sure that my CLI and API were both behaving in the desired way. Tests can be run by running `python3 app.py` in one terminal and in a second `python -m unittest tests/*.py`.
The following is a list of the tests performed:
 - Push
   - Success
     - Assert CLI output is as desired
     - Assert image was successfully added to repository file system
     - Assert image is properly listed using `ls`
   - Success for correct file types
     - Assert Success for files with extensions in `png, jpg, jpeg, gif, pdf`
   - Fail for missing file argument (only tested argument once to assure it was working properly)
     - Assert proper error message
   - Fail for missing local file
     - Assert proper error message
   - Fail for bad file extension
     - Assert proper error message 
 - Pull
   - Success
     - Assert CLI output is as desired
     - Assert new file exists on local system
   - Success custom output file
     - Assert CLI output is as desired
     - Assert new file exists on local system
   - Fail invalid image id
     - Assert proper error message
   - Check that correct file was pulled
     - Push multiple files with different contents and assert each pulled file matches the pushed one
 - Rename
   - Success
     - Assert CLI output is as desired
     - Assert pulled file after rename has new name
   - Fail invalid image id
     - Assert proper error message
   - Fail bad new name
     - Assert new name has proper file extension
 - Remove
   - Success
     - Assert proper error message
     - Assert file is no longer in repository file system
   - Fail invalid image id
     - Assert proper error message
   - Remove confirmation test
     - Assert CLI confirmation output is as desired
 - LS
   - Assert LS displays proper results after doing different adds, deletes, renames
