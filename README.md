# deb_finder

## The Problem

I wanted to take advantage of iron.io's IronWorker service. These workers run in a docker container maintained by iron.io . 

Iron.io has abstracted the configuration of the dockerfile to their own proprietary format. You cannot add RUN apt-get instructions to configure the container. The worker task I wanted to port has quite a few dependencies... No Bueno.

## The Solution

IronWorker's abstraction of a dockerfile config allows you to add/install deb packages.
i.e. deb 'http://mirror.pnl.gov/ubuntu/pool/main/i/imagemagick/libmagickcore5_6.7.7.10-2ubuntu4_amd64.deb'

Ok, but who has the time to look up .deb file locations for 15+ dependencies?! 

ENTER deb_finder

## Usage

The deb_finder script is executed as a standalone Python script.
The script will go through each one of your aptitude packages and find the url to the online .deb archive. It currently prints a list of dicts containing the aptitude package names and their .deb urls. Pick out the ones you need for your PIP requirements.

python deb_finder.py


## Future

This was a quick PoC. I may or may not continue to improve it. 

Things to do:
	*1) Output results to a file
	*2) Figure out how to cut out the cruft debs/deps
	*3) Speed it up, find a faster way to retrieve the .deb url or thread it perhaps.
	*4) Other stuff TBD...


