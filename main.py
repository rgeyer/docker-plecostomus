#!/usr/bin/env python
from docker import Client
from docker.errors import *

cli = Client(base_url='unix://var/run/docker.sock')

exited_containers = cli.containers(all=True, filters={'status': 'exited'})
for container in exited_containers:
    container_id = container.get('Id')
    print "Destroying container "+container_id
    cli.remove_container(container=container_id, force=True)

containers = cli.containers()
image_blacklist = []
for container in containers:
    image = container.get('Image')
    image_blacklist.append(image)
    image_blacklist.append(image+':latest')

print "Blacklisted the following images from deletion "+str(image_blacklist)

images = cli.images()
for image in images:
    imagenames = image.get('RepoTags')
    has_running_containers = (len(set(imagenames).intersection(image_blacklist)) > 0)
    if not has_running_containers:
        image_id = image.get('Id')
        print "Destroying image "+image_id
        try:
            cli.remove_image(image=image_id)
        except APIError as err:
            print "Error destroying {}. Error: {}".format(image_id, err)
