## OVERVIEW

We have a  fairly large volume of data downloaded  from the eBay web site and stored in JSON files. Task is to examine the data and apply the principles of database design in order to implement a good relational schema for it. 
and the Python programs (parser.py and model.py) transforms the data from its JSON form into SQLite’s load file format, conforming to the relational schema.

So,the task is to examine the JSON files completely understand the data and translate this data into relations and load it into the AuctionBase database using the python parser that I developed here.



##  TASK A: Data Modelling
Designing the relational schema for the data presented. The schema is located at in Schema/create.sql

##TASK B: WRITE A DATA TRANSFORMATION PROGRAM
The goal here is to transforms the JSON data into SQLite load files that are consistent with
the relational schema designed. 
parser parses and extract each JSON file and then output the appropriate
SQLite bulk-loading files according to the relational schema.

To parse the full data set, we simply use the command above, but change items-0.json to items-*.json:
python skeleton_parser.py ebay_data/items-*.json


## TASK B: LOAD THE DATA INTO SQLITE
The next step is to create and populate the AuctionBase database. SQLite provides a facility for reading a
set of commands from a file. I am kaing use of this facility for (re)building the database and running sample
queries.

created a command file called load.txt that loads the data into the tables. This file will look
something like:
.separator |
.import items.dat Items
update Items set ... -- Replace all token ‘NULL‘ values with null
.import auctionuser.dat AuctionUser
...

## TASK C: TEST THE SQLITE DATABASE
The final step is to take the newly loaded database for a test drive by running a few SQL queries over it.
We run below sample SQL queries to test the Datbase and verify the results:
1. Find the number of users in the database.
2. Find the number of users from New York (i.e., users whose location is the string "New York").
3. Find the number of auctions belonging to exactly four categories.
4. Find the ID(s) of auction(s) with the highest current price.
5. Find the number of sellers whose rating is higher than 1000.
6. Find the number of users who are both sellers and bidders.
7. Find the number of categories that include at least one item with a bid of more than $100.
