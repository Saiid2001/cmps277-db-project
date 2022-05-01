 Drop Schema if exists Project;

Create Schema Project;

Use Project;

Create Table Organization(
	website Varchar(200) unique,
    oname Varchar(200) unique,
    oemail Varchar(200) Primary Key Not NULL,
    olocation Varchar(200),
    oscore int,
    is_educational boolean,
    is_workplace boolean
);

CREATE VIEW Organization_Name As
    SELECT oemail, oname from Organization;

Create unique index org_name on Organization (oname);

Create Table User(
	fname Varchar(100) Not NULL,
    lname Varchar(100) NOT NULL,
    email Varchar(200) NOT NULL unique primary key,
    pass Varchar(200),
    linked_in Varchar(200),
    phone Varchar(20),
    dob date not null,
    website Varchar(100),
    gender Varchar(6)
);

Create unique index full_name on User (fname, lname);

Create Table Student(
    uemail Varchar(200) NOT NULL,
    sop text,
    is_open_work Boolean,
    Foreign key (uemail) references User(email) On delete cascade
);

Create Table alumnus(
    uemail Varchar(200) NOT NULL,
    score int default 0,
    position Varchar(50),
    work_email Varchar(200) Not Null,
    Foreign key (uemail) references User(email) On delete cascade,
    Foreign key (work_email) references Organization(oemail)On delete cascade
);

Create index workplace on alumnus(work_email);

Create Table Opportunity_Field(
	ofname Varchar(100) Not Null Primary Key,
    description Varchar(3000) 
);

Create Table message(
    receiver_email Varchar(200),
    sender_email Varchar(200),
    content Varchar(3000),
    timestamp timestamp primary key,
    
    Foreign Key(receiver_email) references User(email),
    Foreign Key(sender_email) references User(email)
);

Create index parties on message (receiver_email, sender_email);

Create Table Skills(
	skill Varchar(200),
    semail Varchar(200) NOT NULL,
    Foreign key (semail) references Student(uemail) On delete cascade,
    Primary Key(semail, skill)
);

Create index student_email on Skills (semail);

Create Table Projects(
	date Date,
    name Varchar(200) Not NULL,
    description text,
    semail Varchar(200) NOT NULL,
    Foreign key (semail) references Student(uemail) On delete cascade,
    Primary Key(semail, name, date)
);

Create index s_email on Projects (semail);

Create Table Certifications(
	date Date,
    name Varchar(200) Not NULL,
    url Varchar(100),
    semail Varchar(200) NOT NULL,
    Foreign key (semail) references Student(uemail) On delete cascade,
    Primary Key(semail, url)
);

Create index student_email on Certifications (semail);

Create Table Opportunity(
		id int auto_increment primary key,
		hosting_email Varchar(200) Not NULL,
        name Varchar(200) unique,
		location Varchar(100),
        start_time Date,
        end_time Date,
        app_portal Varchar(300),
        comp_amount int,
        comp_type Varchar(50),
        description text,
        app_deadline Date,
        opp_field Varchar(100),
        alemail Varchar(200) NOT NULL,
        
        Foreign Key(opp_field) references Opportunity_Field(ofname),
        Foreign Key(hosting_email) references Organization(oemail)  on update cascade on delete restrict,
        Foreign Key(alemail) references Alumnus(uemail)
);

Create VIEW opp_info As
    SELECT
        alemail,
        opp_field, 
        hosting_email
    FROM 
        opportunity;

Create Table benefits(
	opp_id int,
    Foreign Key(opp_id) references Opportunity(id) On delete cascade,
    benefit Varchar(200),
    Primary Key(opp_id, benefit)
);

Create Table will_to_work(
    semail Varchar(200) NOT NULL,
    ofname Varchar(100) Not Null,
    Foreign key (semail) references Student(uemail) On delete cascade,
    Foreign key (ofname) references Opportunity_Field(ofname),
    Primary Key(semail, ofname)
);

Create Table apply(
    semail Varchar(200) NOT NULL,
    opp_id int,
    Foreign key (semail) references Student(uemail) On delete cascade,
    Foreign Key(opp_id) references Opportunity(id) On delete cascade,
    Primary Key (semail, opp_id)
);

Create Table Experience(
	id int NOT NULL Primary Key auto_increment,
	position Varchar(50),
    start_date date,
    end_date date,
    alemail Varchar(200) NOT NULL,
    work_email Varchar(200) Not Null,
    Foreign key (alemail) references ALumnus(uemail) On delete cascade,
    Foreign Key (work_email) references Organization(oemail)
);

Create index al_work on Experience(alemail, work_email);

Create Table exp_accomplishments(
	ex_id int Not NULL,
    title Varchar(200) Not Null,
    content Varchar(600),
    Foreign Key (ex_id) references Experience(id) On delete cascade,
    Primary Key (ex_id, title)
);


Create Table Complete_program(
	id int auto_increment primary key, 
	inst_email Varchar(200) Not Null,
    uemail Varchar(200) NOT NULL,
    start_date date,
    end_date date,
    score int,
    major varchar(200),
    is_complete Boolean,
    Foreign Key(inst_email) references Organization(oemail),
    Foreign key (uemail) references User(email) On delete cascade
);

Create Table prg_accomplishments(
	prg_id int Not Null,
    Foreign key (prg_id) references Complete_program(id) On delete cascade,
    title Varchar(200),
    content Varchar(1000),
    Primary Key (prg_id, title)
);

Create Table Mentor(
    mentor_email Varchar(200) NOT NULL,
    mentee_email Varchar(200) NOT NULL,
    start_date date,
    rating int, 
    status Varchar(12),
    Foreign Key (mentor_email) References Alumnus(uemail),
    Foreign Key (mentee_email) References Student(uemail),
    Primary Key(mentor_email , mentee_email, start_date)
);

Create index mentor on Mentor(mentor_email);
Create index mentee on Mentor(mentee_email);

Create Table Associate(
    alemail Varchar(200) NOT NULL,
    opp_id int Not null,
    Foreign Key (alemail) References Alumnus(uemail) On delete cascade,
    Foreign Key (opp_id) References opportunity(id),
    Primary Key(alemail, opp_id)
);