import psycopg2

conn = psycopg2.connect("dbname='postgres' user='Alchemistake'  password='C4NB3GVMA'")
cur = conn.cursor()

cur.execute("""SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE';""")
rows = cur.fetchall()
delete = []
while len(rows):
    print rows
    for r in rows:
        try:
            cur.execute('DROP TABLE "' + r[0] + '";')
            delete.append(r)
        except Exception as e:
            print e
            cur.execute("COMMIT;")
    for d in delete:
        rows.remove(d)
    delete = []

cur.execute("""create table "user" 
(user_id int  primary key,
 user_nickname	varchar(16) not null,
 user_email		varchar(245) not null,
 user_password	varchar(32) not null,
 user_role		int not null);
""")

cur.execute("""create table follow
(follower		int,
 followed		int,
 Primary Key(follower, followed),
 Foreign Key(follower) references "user"(user_id),
 Foreign Key(followed) references "user"(user_id)
 );
""")

cur.execute("""CREATE TABLE block
(blocker		INT,
 blocking		INT,
 PRIMARY KEY(blocker, blocking),
 FOREIGN KEY(blocker) REFERENCES "user"(user_id), 
 FOREIGN KEY(blocking) REFERENCES "user"(user_id));
""")

cur.execute("""CREATE TABLE propose
(proposed		INT,
 proposer		INT,
 PRIMARY KEY(proposed, proposer),
 FOREIGN KEY(proposed) REFERENCES "user"(user_id), 
 FOREIGN KEY(proposer) REFERENCES "user"(user_id));""")

cur.execute("""CREATE TABLE directMessage
(message_id		INT ,
 message		VARCHAR(256) NOT NULL,
 sender_user		INT NOT NULL,
 receiver_user		INT NOT NULL,
 PRIMARY KEY(message_id),
 FOREIGN KEY(sender_user) REFERENCES "user"(user_id), 
 FOREIGN KEY(receiver_user) REFERENCES "user"(user_id));""")

cur.execute("""CREATE TABLE topic
(topic_id		INT ,
 topic_name		VARCHAR(256) NOT NULL,
 topic_date 		DATE NOT NULL,
 creator_user	INT NOT NULL,
 PRIMARY KEY(topic_id),
 FOREIGN KEY(creator_user) REFERENCES "user"(user_id));""")

cur.execute("""CREATE TABLE subtopic
(topic_id		INT,
 subtopic_name	VARCHAR(256),
 adder_user		INT NOT NULL,
 PRIMARY KEY(topic_id, subtopic_name),
 FOREIGN KEY(topic_id) REFERENCES topic(topic_id),
 FOREIGN KEY(adder_user) REFERENCES "user"(user_id));""")

cur.execute("""CREATE TABLE definition
(definition_id	INT ,
 definition_date	DATE NOT NULL,
 definer_user 	INT NOT NULL,
 definition		VARCHAR(256) NOT NULL,
 PRIMARY KEY(definition_id),
 FOREIGN KEY(definer_user) REFERENCES "user"(user_id));""")

cur.execute("""CREATE TABLE post
(post_id		  INT,
 rate_value		INT,
 PRIMARY KEY(post_id),
 FOREIGN KEY(post_id) references definition(definition_id));
""")
cur.execute("""CREATE TABLE enter
(topic_id		INT,
 subtopic_name		VARCHAR(256),
 post_id    INT,
 PRIMARY KEY(subtopic_name,post_id),
 FOREIGN KEY(topic_id) references topic(topic_id),
 FOREIGN KEY(subtopic_name) references subtopic(subtopic_name),
 FOREIGN KEY(post_id) references post(post_id));
""")
cur.execute("""CREATE TABLE rate
(user_id		INT,
 post_id		INT,
 vote			  INT,
 PRIMARY KEY(user_id, post_id),
 FOREIGN KEY(user_id) references user(user_id),
 FOREIGN KEY(post_id) references post(post_id));
""")
cur.execute("""CREATE TABLE comment
(comment_id		INT,
 post_id		  INT,
 PRIMARY KEY(comment_id),
 FOREIGN KEY(comment_id) REFERENCES definition(definiton_id),
 FOREIGN KEY(post_id) REFERENCES post(post_id));
""")
cur.execute("""CREATE TABLE reply
(comment_id		INT,
 replied_comment		INT,
 PRIMARY KEY(comment_id),
 FOREIGN KEY(comment_id) REFERENCES comment(comment_id),
 FOREIGN KEY(replied_comment) REFERENCES post(post_id));
""")

cur.execute("""COMMIT;""")
