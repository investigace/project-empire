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
    + [2.2. Update DNS records](#22-update-dns-records)
    + [2.3. (optional) Set up Amazon S3 bucket for backups](#23-optional-set-up-amazon-s3-bucket-for-backups)
    + [2.4. Set up wiki using docker](#24-set-up-wiki-using-docker)
  * [3. Push data from database to the wiki](#3-push-data-from-database-to-the-wiki)
  * [4. Learn to use other scripts](#4-learn-to-use-other-scripts)
- [Database documentation](#database-documentation)
  * [_0. Introduction_ sheet](#0-introduction-sheet)
  * [_1. Legal entities_ sheet](#1-legal-entities-sheet)
  * [_1.1. Legal entities owners_ sheet](#11-legal-entities-owners-sheet)
  * [_1.2. Legal entities other relationships_ sheet](#12-legal-entities-other-relationships-sheet)
  * [_1.3. Legal entities sources_ sheet](#13-legal-entities-sources-sheet)
  * [_1.4. Legal entities previous names_ sheet](#14-legal-entities-previous-names-sheet)
  * [_1.5. Legal entities previous addresses_ sheet](#15-legal-entities-previous-addresses-sheet)
  * [_1.6. Legal entities media mentions_ sheet](#16-legal-entities-media-mentions-sheet)
  * [_2. People_ sheet](#2-people-sheet)
  * [_2.1. People sources_ sheet](#21-people-sources-sheet)
  * [_3. Subsidies_ sheet](#3-subsidies-sheet)
  * [_3.1. Subsidies payments_ sheet](#31-subsidies-payments-sheet)
  * [_3.2. Subsidies sources_ sheet](#32-subsidies-sources-sheet)
- [Wiki documentation](#wiki-documentation)
- [Scripts documentation](#scripts-documentation)
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

[↑ Jump to Table of Contents](#table-of-contents)

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
$ git clone git@github.com:investigace/project-empire.git
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
$ git clone git@github.com:investigace/project-empire.git
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

[↑ Jump to Table of Contents](#table-of-contents)

---

## Database documentation

We have built the Project Empire database structure to best accommodate all the different data we encountered when mapping business empires and we will explain the structure in the following sections. Scripts and wiki depend on this structure — sheets and columns having correct names and data being in specific format —, but we understand that the needs of your projects can vary and there are safe ways to adjust the structure without breaking any of the scripts and wiki features. Adjusting is explained right after all the database spreadsheet sheets.

* Demo database spreadsheet: https://docs.google.com/spreadsheets/d/1EJ-bP-qqTjZx2jcY6hfG3uAKvn6_FtCA-vqD4qVzn-k/edit
* Empty database spreadsheet: https://docs.google.com/spreadsheets/d/19syMW_V3G6AmG0yIHBZzys2RfBH4zsAbObO5FrhjB68/edit

### _0. Introduction_ sheet

This sheet is only informative and is not used by scripts or wiki at all. Feel free to remove or completely change as you desire.

### _1. Legal entities_ sheet

First of the 3 main sheets, keeping information about legal entities like companies, trusts, etc. Every row in this sheet is one legal entity and its current details.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Database identifier_ | AGROFERT, a.s. | Yes | Unique identification in this database. Should be name of the legal entity. When other sheets are referencing legal entity, they are referencing what is written in this column.<br><br>If there are more legal entities with same name, we recommend to differentiate them by adding explanation to the parenthesis. Eg. if there are two Acme Ltd. companies and one is in United Kingdom and the other in New Zealand, then one could have identifier "Acme Ltd. (UK)" and the other "Acme Ltd. (NZ)" |
| _Legal entity type_ | Company | Yes | Type of legal entity. Whether it is company, trust, etc. Scripts and wiki do not rely on any specific values here, so feel free to differentiate legal entity types by any values you wish. |
| _Name_ | AGROFERT, a.s. | Yes | The actual current name of the legal entity. |
| _Country_ | CZ | Yes | Country where the legal entity is currently founded. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US, etc. |
| _Identification number_ | 26185610 | No | Identification for the legal entity in its country. Can be only number, but also any text, eg. in Germany it can be "Stendal HRB 12345". |
| _Address_ | Pyšelská 2327/2, Chodov, 149 00 Praha 4 | No | Current address of the legal entity. Ideally full, but can be also partial, eg. only city. |
| _Foundation date_ | 2000-07-01 | No | The date when the legal entity was founded. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Dissolution date_ | N/A | No | If the legal entity was dissolved, this is the date when the dissolution happened. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. If the company was not dissolved, we recommend to fill N/A. |
| _Other notes_ | Umbrella company for empire of Andrej Babiš | No | Add any other notes you want for the legal entity in this column. |

### _1.1. Legal entities owners_ sheet

Sheet with information about legal entity owners. Every row in this sheet is one owner record for referenced legal entity. Ownerships are separate from other relationships as they are especially important when mapping the business structure and as the ownerships have the additional _Owned percentage_ column.

Note that there are 2 types of ownership records you can define using this sheet. Either referencing one, which references some legal entity or person you have in the database, or partial one, which does not reference. The partial record can be useful eg. when you want full ownership history for some company, but don't actually want to track all the owners in the database, because some owners are not part of the business empire you are after.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Owned legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity which is being owned. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Owner legal entity or person reference_ | Andrej Babiš | No | If the owner is in the database, fill here _Database identifier_ of either legal entity or person from the database. If the owner is not in the database for any reason, leave empty. |
| _Owner type_ | Person | Yes | Add "Legal entity" when the owner is a legal entity, "Person" when it is a person. |
| _Owner name_ | Andrej Babiš | Yes | Name of the owner, either legal entity name or person name. |
| _Owner country_ | CZ | No | Country of the owner. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US, etc. |
| _Owner address_ | Pyšelská 2327/2, Chodov, 149 00 Praha 4 | No | Current address of the owner. Ideally full, but can be also partial, eg. only city. |
| _Owner legal entity identification number_ | 26185610 | No | If the owner is legal entity, this column is for identification number in its country. Can be only number, but also any text, eg. in Germany it can be "Stendal HRB 12345". |
| _Owner person date of birth_ | 2000-01-01 | No | If the owner is person, this column is for date of birth of that person. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Owned percentage_ | 100 | No | How many percents does the owner owns. Add value from 0 to 100. But also textual values like "Majority" are allowed. |
| _Owned since date_ | 2005-05-30 | No | The date when the ownership started. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Owned until date_ | 2017-02-02 | No | If the ownership ended, this is the date when that happened. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. If the ownership did not end, we recommend to fill N/A. |
| _Ownership details_ | In 2017 transferred ownership to trusts | No | Add any other notes you want for the ownership in this column. |

### _1.2. Legal entities other relationships_ sheet

Sheet with information about other legal entity relationships than ownerships. Every row in this sheet is one relationship to some other legal entity or person, for example who was director of legal entity.

Note that there are 2 types of relationship records you can define using this sheet. Either referencing one, which references some legal entity or person you have in the database, or partial one, which does not reference. The partial record can be useful eg. when you want full relationship history for some company, but don't actually want to track all the related people and legal entities in the database, because some of those are not part of the business empire you are after.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity for which this relationship is defined. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Related legal entity or person reference_ | Andrej Babiš | No | If the related legal entity or person is in the database, fill here _Database identifier_ of their row in the database. If the legal entity or person is not in the database for any reason, leave empty. |
| _Related type_ | Person | Yes | Add "Legal entity" when the relationship is with a legal entity, "Person" when it is with a person. |
| _Related name_ | Andrej Babiš | Yes | Name of the related legal entity or person. |
| _Related country_ | CZ | No | Country of the related legal entity or person. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US, etc. |
| _Related address_ | Pyšelská 2327/2, Chodov, 149 00 Praha 4 | No | Current address of the related legal entity or person. Ideally full, but can be also partial, eg. only city. |
| _Related legal entity identification number_ | 26185610 | No | If the relationship is with legal entity, this column is for identification number in its country. Can be only number, but also any text, eg. in Germany it can be "Stendal HRB 12345". |
| _Related person date of birth_ | 2000-01-01 | No | If the relationship is with person, this column is for date of birth of that person. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Related since date_ | 2005-05-30 | No | The date when the relationship started. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Related until date_ | 2017-02-02 | No | If the relationship ended, this is the date when that happened. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. If the relationship did not end, we recommend to fill N/A. |
| _Relationship details_ | Chairman of the board | No | Add any other notes you want for the relationship in this column. |

### _1.3. Legal entities sources_ sheet

Sheet with sources of information about legal entities. If you don't need structured sources, it is enough to list sources in _Other notes_ of legal entity. Every row in this sheet is one source used to gain information about a legal entity.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity this source belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Source summary_ | Veřejný Rejstřík a Sbírka Listin - Ministerstvo Spravedlnosti České Republiky. Justice.cz. | No | Summary or name of the source document. |
| _Information gained from source_ | Company identifier, names, addresses, foundation date | No | What kind of information was obtained from the source. |
| _Source last checked date_ | 2020-07-06 | No | The date when the source was last checked. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Source URL_ | https://or.justice.cz/ias/ui/rejstrik-firma.vysledky?subjektId=525681&typ=UPLNY | No | Full URL of the source document. |

### _1.4. Legal entities previous names_ sheet

Sheet for previous names of legal entities. You might not need previous names this much structured, but structure here can be useful when searching for historical records where the legal entity can be using some previous name.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Legal entity reference_ | SynBiol, a.s. | Yes | Legal entity this previous name belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Previous name_ | SYNTHESIA a.s. | Yes | Previous name of the legal entity. |
| _Named since date_ | 2004-11-08 | No | The date the legal entity gained this name. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Named until date_ | 2006-03-27 | No | The date the legal entity lost this name. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |

### _1.5. Legal entities previous addresses_ sheet

Sheet for previous addresses of legal entities. You might not need previous addresses this much structured, but structure here can be useful when searching for historical records where the legal entity can be using some previous address.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity this previous address belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Previous address_ | Pyšelská 1234, Chodov, 149 00 Praha 4 | Yes | Previous address of the legal entity. |
| _Address since date_ | 2004-11-08 | No | The date the legal entity gained this address. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |
| _Address until date_ | 2006-03-27 | No | The date the legal entity lost this address. When full date, it must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. But if you don't have the full date, it is ok to just have year here. |

### _1.6. Legal entities media mentions_ sheet

Sheet for information about mentions of legal entity in media. Every row in this sheet is one mention in media.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity this media mention belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Summary of the media mention_ | Wikipedia page | No | Summary or name of the mention in media. |
| _Media last checked date_ | 2022-01-01 | No | The date when the mention was last checked. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Media mention url_ | https://cs.wikipedia.org/wiki/Agrofert | No | Full URL of the mention in media. |

### _2. People_ sheet

Second of the 3 main sheets, keeping information about people. Every row in this sheet is one person and their current details.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Database identifier_ | Andrej Babiš | Yes | Unique identification in this database. Should be name of the person. When other sheets are referencing person, they are referencing what is written in this column.<br><br>If there are more people with same name, we recommend to differentiate them by adding year of birth in the parenthesis. Eg. if there are two persons with name John Doe and one is born in 1950 and the other in 1980, then one would have identifier "John Doe (1950)" and the other "John Doe (1980)" |
| _Full name_ | Andrej Babiš | Yes | Full name of the person. Last name should be at the end. |
| _Nationality_ | CZ | No | Nationality of the person. Does not support multiple nationalities, so use _Other notes_ to track nationalities of multinationals. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US, etc. |
| _Date of birth_ | 2000-01-01 | No | The date of birth. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. Full date of birth is not published in the wiki, only the year. |
| _Residence country_ | CZ | No | Country of the person's residence. Must be two-letter country code defined by standard [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Eg. Germany is DE, France is FR, United States are US, etc. |
| _Residence full address_ | Pyšelská 2327/2, Chodov, 149 00 Praha 4 | No | Current address of the person's residence. Ideally full, but can be also partial, eg. only city. Full address is not published in the wiki, only value in column _Residence only city_. |
| _Residence only city_ | Praha 4 | No | City from the current address of the person's residence. |
| _Other notes_ | Former prime minister of Czechia | No | Add any other notes you want for the person in this column. |

### _2.1. People sources_ sheet

Sheet with sources of information about people. If you don't need structured sources, it is enough to list sources in _Other notes_ of person. Every row in this sheet is one source used to gain information about a person.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Person reference_ | Andrej Babiš | Yes | Person this source belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _2. People_. |
| _Source summary_ | AGROFERT INC. :: Massachusetts (US) :: OpenCorporates. Opencorporates.Com. | No | Summary or name of the source document. |
| _Information gained from source_ | Connection to AGROFERT INC. | No | What kind of information was obtained from the source. |
| _Source last checked date_ | 2020-07-06 | No | The date when the source was last checked. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Source URL_ | https://opencorporates.com/companies/us_ma/383446187 | No | Full URL of the source document. |

### _3. Subsidies_ sheet

Third of the 3 main sheets, keeping information about subsidies. Every row in this sheet is one subsidy and its details. Note that this sheet does not have any amount columns, because the subsidies are often split into more payments from different providers or in different years and we keep the amounts on the payments only.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Database identifier_ | CEDR-30/04UL-2003 | Yes | Unique identification in this database. Should be ideally project code. When other sheets are referencing subsidy, they are referencing what is written in this column.<br><br>If there are more subsidies with same project code, we recommend to differentiate them by adding something in the parenthesis. Eg. if there are two subsidies with code A-123 and one is from 2010 and the other from 2015, then one would have identifier "A-123 (2010)" and the other "A-123 (2015)" |
| _Receiving legal entity reference_ | AGROFERT, a.s. | Yes | Legal entity which received this subsidy. Should have exactly the same value as _Database identifier_ of some row in sheet _1. Legal entities_. |
| _Year_ | 2002 | No | Year in which the subsidy was received. Could be also range of years like "2007-2013". |
| _Project name_ | Zlepšení hygieny provozu při skladování drůbeže  | No | Name of the subsidized project. |
| _Project code_ | 30/04UL-2003 | No | Code of the subsidized project. |
| _Programme name_ | SAPARD | No | Name of the programme the subsidy was received from. |
| _Programme code_ | SAPARD | No | Code of the programme the subsidy was received from. |
| _Notes_ | Signed in 2002, carried out in 2003. | No | Add any notes you want for the subsidy in this column. |

### _3.1. Subsidies payments_ sheet

Sheet for keeping information about subsidy payments. Every row in this sheet is payment from one provider in given year belonging to some subsidy.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Subsidy reference_ | CEDR-30/04UL-2003 | Yes | Subsidy this payment belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _3. Subsidies_. |
| _Provider_ | Czech Ministry of agriculture | No | Institution which provided this payment. |
| _Year_ | 2003 | No | Year the payment was made. |
| _Original currency_ | CZK | No | The original currency of the payment. Must be three-letter code defined by standard [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217). Eg. Euro is EUR, US dollar is USD, Pound sterling is GBP, etc. |
| _Amount in original currency_ | 556,875.00 | No | Amount of the payment in the original currency. Must be either in the English notation (12,345.67) or without any notation (12345). |
| _Amount in EUR_ | 22,736.00 | No | Amount of the payment in Euro. Must be either in the English notation (12,345.67) or without any notation (12345). |
| _Notes_ | Using approximate exchange rate 24,49 CZK/EUR. | No | Add any notes you want for the payment in this column. |

### _3.2. Subsidies sources_ sheet

Sheet with sources of information about subsidies. If you don't need structured sources, it is enough to list sources in _Notes_ of subsidy. Every row in this sheet is one source used to gain information about a subsidy.

| Column | Example value | Required | Explanation |
| ------ | ------------- | -------- | ----------- |
| _Subsidy reference_ | CEDR-30/04UL-2003 | Yes | Subsidy this source belongs to. Should have exactly the same value as _Database identifier_ of some row in sheet _3. Subsidies_. |
| _Source summary_ | Subsidy record on Hlídač státu | No | Summary or name of the source document. |
| _Information gained from source_ | Full subsidy record | No | What kind of information was obtained from the source. |
| _Source last checked date_ | 2021-04-28 | No | The date when the source was last checked. Must be in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format, which is YYYY-MM-DD. |
| _Source URL_ | https://www.hlidacstatu.cz/Dotace/Detail/cedr-a85110a7e99bbff7370eebb382f90913c193db91 | No | Full URL of the source document. |

### Adjusting structure

TODO

[↑ Jump to Table of Contents](#table-of-contents)

---

## Wiki documentation

### Restore wiki from S3 backup

[↑ Jump to Table of Contents](#table-of-contents)

---

## Scripts documentation

[↑ Jump to Table of Contents](#table-of-contents)

---
## License

Everything in this repository is licensed under [GNU General Public License v3.0](https://github.com/investigace/project-empire/blob/main/LICENSE).

[↑ Jump to Table of Contents](#table-of-contents)

