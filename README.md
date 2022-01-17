# Project Empire

Project Empire is a database project concentrating information about assets and companies of influential Czech oligarchs. The business structures of the Central European oligarchs are vast and intransparent, spanning many countries. Therefore, a database is developed, which makes the data accessible. The project serves the public, journalists, researchers, civil society or any other interested users across Europe. It helps to understand how economic, political and media power is being monopolized in Central Europe.

Project was created by [České centrum pro investigativní žurnalistiku, o.p.s.](https://www.investigace.cz/) and between September 2021 and January 2022 was funded by [Stars4Media innovation programme](https://stars4media.eu/).

Currently running Project Empire wikis:

| Person of interest | Project Empire wiki              |
| ------------------ | -------------------------------- |
| Andrej Babiš       | https://noveimperiumab.vlki.cz/ (UPDATE WITH FINAL DOMAIN) |
| Daniel Křetínský   |  https://empirekretinsky.vlki.cz/ (UPDATE WITH FINAL DOMAIN)  |

If you have any questions related to this project, please contact (FILL EMAIL)

## Table of contents

- [How Project Empire works?](#how-project-empire-works)
  * [Database](#database)
  * [Wiki](#wiki)
  * [Scripts](#scripts)
- [How to use Project Empire?](#how-to-use-project-empire)
  * [1. Start your database](#1-start-your-database)
  * [2. Install wiki](#2-install-wiki)
  * [3. Push data from database to the wiki](#3-push-data-from-database-to-the-wiki)
  * [4. Learn to use other scripts](#4-learn-to-use-other-scripts)
- [License](#license)

## How Project Empire works?

There are 3 main parts to a working Project Empire. **Database**, which is a Google spreadsheet containing all the data about business structures of selected person of interest. **Wiki**, which makes it possible to publicly browse through the database. And **scripts**, which most importantly offer a way to push data from the database to wiki.

Let's show all the parts using demo data. We have put together tiny sample from our first database done for Andrej Babiš. Here are links for both the database and wiki:

* Demo database: https://docs.google.com/spreadsheets/d/1EJ-bP-qqTjZx2jcY6hfG3uAKvn6_FtCA-vqD4qVzn-k/edit
* Demo wiki: https://project-empire-wiki-demo.vlki.cz/

### Database

If you open the database, you can see that on the first sheet there is an introduction to that specific database. In our sample database we have 6 legal entities, 2 people and 2 subsidies. All the data is then organized in separate sheets.

If you are interested in the legal entities like companies, trusts, etc., you can browse them in the sheet "1. Legal entities". People are in sheet "2. People" and subsidies in "3. Subsidies". The rest of sheets are additional information for each of these base data types.

One of the important parts of databases with business structures is keeping the relationships between legal entities and people. You can find these in sheets "1.1. Legal entities owners" and "1.2. Legal entities other relationships". It is important to keep the data organized like this as the scripts rely on the structure.

Normally the database would not be publicly available, but only shared to people collaborating on the data. That's why part of Project Empire is also wiki, which allows publishing the database for anyone to browse through.

### Wiki

Project Empire wiki is a custom-configured [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) which is prepared to be run via [Docker](https://www.docker.com/) anywhere you want — in the cloud or on your server. After installing, you can customize it yourself to present your data exactly how you want.

You can see that the [demo wiki](https://project-empire-wiki-demo.vlki.cz/) right now contains the same number of legal entities, people and subsidies as the database. And if you open for example the company [AGROFERT, a.s.](https://project-empire-wiki-demo.vlki.cz/index.php/AGROFERT,_a.s.), you can see, apart from the basic information, all the owner and other relationships the company has and media mentions from the database together at that one page. Plus offers links to the related pages. There lies the value of the wiki — it displays the data clearly and in easily browsable fashion.

But how you get the data from the database to the wiki? The data don't have to be manually updated, we have a script, which is takes the database spreadsheet and pushes its data to the wiki.

### Scripts

There are few different scripts as part of Project Empire, which all help with gathering data about business structures, but the most important script is definitely the one pushing the data from the database to the wiki.

The script is a Python command line script, so you have to be at least slightly versed in running command line scripts to be able to use it, even though we tried to simplify its usage as much as possible. The process is then that you clone this GitHub repository to your machine, set up Python virtual environment and just run the script.

And that's it. That's the whole Project Empire. If you want to install it and play with it yourself, you can find the documentation for it below.

## How to use Project Empire?

### 1. Start your database

(TODO)

### 2. Install wiki

(TODO)

### 2.1. Set up server with docker and docker-compose

(TODO: offer setup of virtual server on Google Cloud, AWS and Digital ocean)

### 2.2. Update DNS records

(TODO: show what DNS records needs to be changed for primary or secondary domain set up)

### 2.3. (optional) Set up Amazon S3 bucket for backups

(TODO)

### 2.4. Set up wiki using docker

(TODO)

### 3. Push data from database to the wiki

(TODO)

### 4. Learn to use other scripts

(TODO)

## License

Everything in this repository is licensed under [GNU General Public License v3.0](https://github.com/vlki/project-empire/blob/main/LICENSE).

