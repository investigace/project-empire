# Set up wiki server on DigitalOcean

## 1. Create droplet

Start with creating droplet. On the top:

* Make sure Ubuntu 20.04 selected.
* If you are not expecting heavy traffic, the smallest droplet with 1 CPU, 1 GB and 25 GB SSD disk is enough for running Project Empire wiki.

![](/docs/screenshots/create-droplet-1.png?raw=true)

Further along select the datacenter you need, we recommend the physically closest one for fast connection.

![](/docs/screenshots/create-droplet-2.png?raw=true)

Then make sure you have your SSH key added so you can use it later to connect to the server from console.

![](/docs/screenshots/create-droplet-2.png?raw=true)

You don't have to touch other defaults, so just hit "Create droplet".

## 2. Install docker and docker-compose

When droplet is created, use the SSH key to connect to the server as a root. When connected, install first `docker` and then `docker-compose`.

You can install `docker` by following commands in the first step of this DigitalOcean guide: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

Regarding `docker-compose`, follow commands in the first step of another DigitalOcean guide: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

After the two, you should have `docker` service running and `docker-compose` command available on the server. And that's it, now the server is prepared for installation of Project Empire wiki.
