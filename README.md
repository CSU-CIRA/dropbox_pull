## Overview

Download files stored in a shared Dropbox folder

## Obtaining the code
Clone this repository to your local machine using `git clone https://github.com/CSU-CIRA/dropbox_utils.git.git`

## Creating a Dropbox API Access Token
[OAuth Guide](https://www.dropbox.com/lp/developers/reference/oauth-guide)

## Run instructions
### Environment set up
This tool is intended to run in an environment described by
the Dockerfile in this repository: a basic python environment
with the dropbox module installed with
[conda](https://anaconda.org/anaconda/dropbox) or [pip](https://www.dropbox.com/developers/documentation/python#install)

### Building the image
To use Docker, build the image using the command `docker build -t dropbox:1.0 .`
Although the tag (`-t`) is optional, it will assign a name and version to
the resulting image which will make it easily locatable and also provide
a mechanism to have multiple versions available for testing and using
upgrades. Note the `.` assumes you are working in the directory that
contains the Dockerfile. To provide an alternate path, trade the period
out for `-f /path/to/the/Dockerfile`

### Creating a container from the image
Although the default Docker behavior will create a container that runs
as root, it is best practice to declare your own user when you create
the container to avoid messy security issues. For compatability with
the host machine, you can use your user and preferred group ids in the
container, or if compatability is not an issue, you may simply create a new user:group identification for the container. To get your user and group id
on the host (provided that you are working in a linux-like environment), use
`id`.

To create and run a container from the image, use
`docker run -it --name dropbox_devel -u uid:gid -v
/path/to/data/on/host:/path/to/data/in/the/container dropbox:1.0`,
adding -v flags before the image name as necessary to provide any data
mounts needed for the code to be able to access the necessary output
data and access token file. Again, the `--name` is optional but makes
the container easily locatable.

### Entering the container
The `-it` flag in the `docker build` command will start an interactive
session within the container, where you will be dropped in the
`/dropbox_apps` directory where the conversion scripts are located.
If the container is stopped (you can check by running `docker ps`),
start it by running `docker start dropbox_devel` and then enter it
using `docker exec -it dropbox_devel /bin/bash`.

### Running the Python scripts
#### dropbox_pull.py
- Get help: 
```
python dropbox_pull.py -h
```
- Pull all files from shared Dropbox folder:
```
python dropbox_pull.py 
    -d Dropbox URL 
    -o /path/to/put/files/locally
    -t /path/to/text/file/with/dropbox/token 
    -v Include if you want messages printed to stdout
```

