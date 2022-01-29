# Project Empire

Project Empire is a set of tools designed to help with keeping information about assets and companies of inluential people or groups. It was originally created for business structures of former prime minister and owner of vast business empire Andrej Babiš, but is now generalized and can be used for anybody else.

Project was created by [České centrum pro investigativní žurnalistiku, o.p.s.](https://www.investigace.cz/) and between September 2021 and January 2022 was funded by [Stars4Media innovation programme](https://stars4media.eu/).

Currently running Project Empire wikis:

| Person of interest | Project Empire wiki              |
| ------------------ | -------------------------------- |
| Andrej Babiš       | https://noveimperiumab.vlki.cz/ (UPDATE WITH FINAL DOMAIN) |
| Daniel Křetínský   |  https://empirekretinsky.vlki.cz/ (UPDATE WITH FINAL DOMAIN)  |

If you have any questions related to this project, please contact [it@investigace.cz](mailto:it@investigace.cz).

## Table of contents

- [How Project Empire works?](#how-project-empire-works)
  * [Database](#database)
  * [Wiki](#wiki)
  * [Scripts](#scripts)
- [How to use Project Empire?](#how-to-use-project-empire)
  * [1. Start your database](#1-start-your-database)
  * [2. Install wiki](#2-install-wiki)
    + [2.1. Set up server with docker and docker-compose](#21-set-up-server-with-docker-and-docker-compose)
    + [2.2. Update DNS records](22-update-dns-records)
    + [2.3. (optional) Set up Amazon S3 bucket for backups](#23-optional-set-up-amazon-s3-bucket-for-backups)
    + [2.4. Set up wiki using docker](#24-set-up-wiki-using-docker)
  * [3. Push data from database to the wiki](#3-push-data-from-database-to-the-wiki)
  * [4. Learn to use other scripts](#4-learn-to-use-other-scripts)
- [License](#license)

---

## How Project Empire works?

There are 3 main parts to a working Project Empire. **Database**, which is a Google spreadsheet containing all the data about business structures of selected person of interest. **Wiki**, which makes it possible to publicly browse through the database. And **scripts**, which most importantly offer a way to push data from the database to wiki.

Let's show all the parts using demo data. We have put together tiny sample from our first database done for Andrej Babiš. Here are links for both the database and wiki:

* Demo database: https://docs.google.com/spreadsheets/d/1EJ-bP-qqTjZx2jcY6hfG3uAKvn6_FtCA-vqD4qVzn-k/edit
* Demo wiki: https://project-empire-wiki-demo.vlki.cz/

### Database

If you open the database, you can see that on the first sheet there is an introduction to that specific database. In our demo database we have 6 legal entities, 2 people and 2 subsidies. All the data is then organized in separate sheets.

If you are interested in the legal entities like companies, trusts, etc., you can browse them in the sheet _1. Legal entities_. People are in sheet _2. People_ and subsidies in _3. Subsidies_. The rest of sheets are additional information for each of these base data types.

One of the important parts of databases with business structures is keeping the relationships between legal entities and people. You can find these in sheets _1.1. Legal entities owners_ and _1.2. Legal entities other relationships_. It is important to keep the data organized like this as the scripts rely on the structure.

Normally the database would not be publicly available, but only shared to people collaborating on the data. That's why part of Project Empire is also wiki, which allows publishing the database for anyone to browse through.

### Wiki

Project Empire wiki is a custom-configured [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) which is prepared to be run via [Docker](https://www.docker.com/) anywhere you want — in the cloud or on your server. After installing, you can customize it yourself to present your data exactly how you want.

You can see that the [demo wiki](https://project-empire-wiki-demo.vlki.cz/) right now contains the same number of legal entities, people and subsidies as the database. And if you open for example the company [AGROFERT, a.s.](https://project-empire-wiki-demo.vlki.cz/index.php/AGROFERT,_a.s.), you can see, apart from the basic information, all the owner and other relationships the company has and media mentions from the database together at that one page. Plus offers links to the related pages. There lies the value of the wiki — it displays the data clearly and in easily browsable fashion.

But how you get the data from the database to the wiki? The data don't have to be manually updated, we have a script, which is takes the database spreadsheet and pushes its data to the wiki.

### Scripts

There are few different scripts as part of Project Empire, which all help with gathering data about business structures, but the most important script is definitely the one pushing the data from the database to the wiki.

The script is a Python command line script, so you have to be at least slightly versed in running command line scripts to be able to use it, even though we tried to simplify its usage as much as possible. The process is then that you clone this GitHub repository to your machine, set up Python virtual environment and just run the script.

And that's it. That's the whole Project Empire. If you want to install it and play with it yourself, you can find the documentation for it below.

---

## How to use Project Empire?

### 1. Start your database

First step in using Project Empire is to set up the database. Since the database is a simple Google spreadsheet, you can do that by making a copy of either the demo database spreadsheet or the empty database spreadsheet. You should be able to make a copy by opening the spreadsheet, clicking option _File > Make a copy_ and filling information about your new spreadsheet.

* Demo database spreadsheet: https://docs.google.com/spreadsheets/d/1EJ-bP-qqTjZx2jcY6hfG3uAKvn6_FtCA-vqD4qVzn-k/edit
* Empty database spreadsheet: https://docs.google.com/spreadsheets/d/19syMW_V3G6AmG0yIHBZzys2RfBH4zsAbObO5FrhjB68/edit

After the copy is created, fill your person or group of interest on sheet _0. Introduction_ and then continue with updating data on the other sheets.

We recommend sharing the spreadsheet only to the specific people who will be collaborating on the data and not share it publicly as it may contain sensitive information.

### 2. Install wiki

Next step is installing Project Empire wiki. As mentioned before, wiki is a custom-configured [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) which is prepared to be run via [Docker](https://www.docker.com/). We chose Docker as that way it can be safely run the same even on different systems.

### 2.1. Set up server with docker and docker-compose

Start the installation by setting up a server preferrably running latest Ubuntu (at the time of writing the Ubuntu LTS version was 20.04), with docker and docker-compose installed, SSH access, public IPv4 address and reachable HTTP (80) and HTTPS (443) ports. It can be your own physical server as well as server set up at some cloud platform.

We expect that you are able to set up a server like that, but if not, [here is a tutorial how to set up such server on DigitalOcean](/docs/set_up_wiki_server_on_digitalocean.md).
### 2.2. Update DNS records

Continue with picking the domain where you want the wiki to be run, you will need to update DNS records for it. The wiki is prepared to be run on either separate domain (e.g. project-empire-wiki.org) or subdomain (e.g. project-empire-wiki.example.org). In case of separate domain, you want to create two A records pointing to the public IPv4 address of server, one for the plain domain and one for www subdomain (wiki takes care of the redirecting then). In case of subdomain, you want one A record for that subdomain pointing to the public IPv4 address of the server.

Example: If the server has public IPv4 address 1.2.3.4 and you want the wiki to run at subdomain project-empire-wiki.example.org, add A record for project-empire-wiki.example.org with value 1.2.3.4.

After changing the DNS records please wait for them to propagate before continuing with the installation, because obtaining HTTPS certificates from Lets Encrypt depends on server being accessible at the picked domain or subdomain.

### 2.3. (optional) Set up Amazon S3 bucket for backups

Optionally, you can create [Amazon S3](https://aws.amazon.com/s3/) bucket for backups of the wiki. Empire data in the wiki obviously does not have to be backed up, because they can always be repushed from database spreadsheet, but other wiki settings like uploaded images, custom pages, etc. would be gone if something happens to your server. Note that together with the bucket you need to create also user with the programmable access via Access key ID and Secret access key.

Even though this step is optional, wee strongly recommend creating Amazon S3 bucket for the backups.

### 2.4. Set up wiki using docker

When you have a server and, optionally, backup bucket set up, it is time for the actual installation of Project Empire wiki.

First, you will need to clone this repository to the server. For example in the home folder of the logged-in user run following:

```
$ git clone git@github.com:vlki/project-empire.git
```

That should create `project-empire` folder with `wiki` folder inside. Go to the wiki folder.

```
$ cd project-empire/wiki
```

Next is providing the configuration. Copy `.env.example` and rename the copy to `.env`. After that, edit `.env` with editor of your choice and fill in your configuration. Here we will be using `vim`.

```
$ cp .env.example .env
$ vim .env
```

Each of the configuration options in `.env` is explained, so go through each of them and set them as you need. When finished, save the changes to the `.env` file and close it.

Now we run the installation. We recommend running it as root, so type in following:

```
$ sudo su
$ docker-compose up
```

That should build images of all the wiki services, create docker containers and run them. Note that it can take few minutes to finish. If everything is fine, the output should end with similar to following:

![](/docs/screenshots/wiki-installation.png?raw=true)

At this point, the wiki is installed and running at your picked domain, but without correct certificates - if you navigate to the domain in the browser you should see warning. That is to be expected, because the certificates were just obtained from Lets Encrypt and nginx service needs to be restarted to load them. Since you cannot run the wiki in the terminal forever anyway, we will restart the wiki as daemon.

First hit Ctrl+C to stop current running services (you might have to wait a bit till they stop), And when that is done, type in following, which will start the services as daemon in background.

```
$ docker-compose up -d
```

Now if you navigate to the domain in your browser, you should see your Project Empire wiki without any warnings, ready to be used.

### 3. Push data from database to the wiki

When you have wiki running, next step is to push there the data from the database. We have prepared for it script written in Python you have to run on your machine. Subsequent instructions expect *nix system, so if you are on Windows machine, run them in Windows Subsystem for Linux (WSL).

To be able to run the script, you first need to make sure you have Python of at least version 3.8 and have it available in terminal. To check both you can run following command to get the Python version:

```
$ python3 --version
```

Continue with cloning this repository to your machine and then open the `scripts` folder in the repository

```
$ git clone git@github.com:vlki/project-empire.git
$ cd project-empire/scripts
```

We are using Python's virtual environment to separate all the libraries needed by scripts from other libraries you might have installed on your system. To initialize the virtual environment, run inside `scripts` folder:

```
$ python3 -m venv .venv
$ . .venv/bin/activate
```

When inside virtual environment, install the libraries:

```
$ pip3 install -r requirements.txt
```

Now you should be set up to actually run the scripts. Note that next time you want to run the scripts, you don't need to fully initialize the virtual environment, it is enough to just run `. .venv/bin/activate`.

The script for pushing data from the database currently cannot read data directly from Google spreadsheet, so to provide data you first need to download spreadsheet as Microsoft Excel file. Open your database Google spreadsheet, click option `File > Download > Microsoft Excel (.xlsx)` and save the Excel file somewhere on your system.

Let's finally push the data. The script `push_empire_database_to_wiki.py` takes 3 arguments, path to the database Excel file, domain of the wiki and wiki user to use. Here is an example how we run it for the demo:

```
$ ./push_empire_database_to_wiki.py ~/Downloads/Project\ Empire\ -\ Demo\ \(Andrej\ Babiš\).xls project-empire-wiki-demo.vlki.cz admin
```

After that the script asks for password of the wiki user. When correct, the script will compute all the needed changes to the wiki pages and asks whether to do the actual changes. Here is an example of output when the script was first run for the demo:

```
$ ./push_empire_database_to_wiki.py ~/Downloads/Project\ Empire\ -\ Demo\ \(Andrej\ Babiš\).xlsx project-empire-wiki-demo.vlki.cz admin
Password for user admin at Empire wiki https://project-empire-wiki-demo.vlki.cz/: ********************
Loaded Empire database: 6 legal entities, 2 people, 0 subsidies
Connected to Empire wiki
Preparing changes to be pushed...

Prepared following changes:

Pages to be created:
  AB private trust I
  AB private trust II
  AGROFERT, a.s.
  AGROFERT, a.s. (1994-2005)
  Agrofert USA, Inc.
  SynBiol, a.s.
  Andrej Babiš
  Zbyněk Průša

Pages to be updated:
  Legal entities overview
  People overview
  Template:Empire summary table

Are you sure you want to push these to Empire MediaWiki? (y/n)
```

If the changes look correct to you, you can type in `y` and that will push all the changes to wiki. Typing in `n` or anything else will stop the script.

And that's it. Congratulations! After pushing is done, you should be able to see all the data in the wiki.

Note that you have to run the script anytime you want to publish updated data from the database to wiki.

---

## Database documentation

We have built the Project Empire database structure to best accommodate all the different data we encountered when mapping business empires and we will explain the structure in the following sections. Scripts and wiki depend on this structure — sheets and columns having correct names and data being in specific format —, but we understand that the needs of your projects can vary and there are safe ways to adjust the structure without breaking any of the scripts and wiki features. Adjusting is explained right after all the database spreadsheet sheets.

### _0. Introduction_ sheet

This sheet is only informative and is not used by scripts or wiki at all. Feel free to remove or completely change as you desire.

### _1. Legal entities_ sheet

First of the 3 main sheets keeping information about legal entities like companies, trusts, etc. Every row in this sheet is one legal entity and its current details.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Database identifier_ | AGROFERT, a.s. | Yes | Unique identification in this database. Should be name of the legal entity. When other sheets are referencing legal entity, they are referencing what is written in this column.<br><br>If there are more legal entities with same name, we recommend to differentiate them by adding explanation to the parenthesis. Eg. if there are two Acme Ltd. companies and one is in United Kingdom and the other in New Zealand, then one would could have identifier "Acme Ltd. (UK)" and the other "Acme Ltd. (NZ)" |
| _Legal entity type_ | Company | Yes | Type of legal entity. Whether it is company, trust, etc. Scripts and wiki do not rely on any specific values here, so feel free to differentiate legal entity types by any values you wish. |
| _Name_ | AGROFERT, a.s. | Yes | The actual current name of the legal entity. |
| _Country_ | CZ | Yes | Country where the legal entity is currently founded. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US. |
| _Identification number_ | 26185610 | No | Identification for the legal entity in its country. Can be only number, but also any text, eg. in Germany it can be "Stendal HRB 12345". |
| _Address_ | Pyšelská 2327/2, Chodov, 149 00 Praha 4 | No | Current address of the legal entity. Ideally full, but can be also partial, eg. only city. |
| _Foundation date_ | 2000-07-01 | No | The date when the legal entity was founded. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Dissolution date_ | N/A | No | If the legal entity was dissolved, this is the date when the dissolution happened. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. If the company was not dissolved, we recommend to fill N/A. |
| _Other notes_ | Umbrella company for empire of Andrej Babiš | No | Add any other notes you want for the legal entity in this column. |

### _1.1. Legal entities owners_ sheet

TODO

### _1.2. Legal entities other relationships_ sheet

TODO

### _1.3. Legal entities sources_ sheet

TODO

### Adjusting structure

TODO

---

## Wiki documentation

### Restore wiki from S3 backup

---

## Scripts documentation

---
## License

Everything in this repository is licensed under [GNU General Public License v3.0](https://github.com/vlki/project-empire/blob/main/LICENSE).

