##makings of tables and insertions to database

import psycopg2
conn = psycopg2.connect(database="charity", user = "admin", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()


###Creation of tables
cur.execute('''
    create table Charity_organization(
    COID integer primary key,
    Name varchar(50) not null unique,
    PostalCode varchar(15) not null ,
    Address varchar(100) not null ,
    PhoneNumber varchar(15) not null
);
''')

cur.execute('''
    create table Financial_aid(
    FID integer primary key,
    Amount integer not null,
    Unit varchar(20),
    Date varchar(20)
);
''')

cur.execute('''
  create table Campaign(
  CID integer primary key,
  Name varchar(50) not null unique,
  Bank_account_number varchar(20) not null,
  Address varchar(100) not null ,
  Purpose varchar(200) not null ,
  COID  integer references Charity_organization(COID),
  GoalID integer references Financial_aid(FID)


);
''')

cur.execute('''
create table Destitute(
    SSN integer primary key,
    First_name varchar(50) not null,
    Last_name varchar(50) not null,
    Date_of_birth timestamp not null,
    Care_takerId integer references Destitute(SSN),
    CampaignID integer references Campaign(CID)
);
''')

cur.execute('''
    create table Destitute_reason(
    SSN integer references Destitute(SSN),
    Reason varchar(200) not null,
    primary key (ssn,Reason)
    );

''')



cur.execute('''
    create table Non_cash_aid(
    NCID integer primary key,
    Value integer not null,
    Unit varchar(20) not null,
    Name varchar(40) not null,
    Number integer not null
    );
''')


cur.execute('''
    create table Member(
    SSN integer primary key ,
    User_name  varchar(20) not null,
    First_name varchar(50) not null,
    Last_name varchar(50) not null,
    Date_of_birth timestamp not null,
    Email varchar(100) not null,
    Password varchar(40) not null
    );
''')

cur.execute('''

create table Employee(
    SSN integer primary key references Member(SSN),
    Date_of_entry timestamp not null,
    Field varchar(40) not null,
    salary integer not null,
    COID integer references Charity_organization(COID)
);
''')

cur.execute('''
    
    create table Worker(
    SSN integer primary key references Member(SSN),
    Date_of_entry timestamp not null,
    Field varchar(40) not null,
    CID integer references Campaign(CID)
);
''')
cur.execute('''
    create table  NCDonate (
    SSN integer references Member(SSN),
    NCID integer references  Non_cash_aid(NCID),
    CID integer references Campaign(CID),
    primary key (SSN, NCID, CID)
);
''')

cur.execute('''
    create table  FDonate (
    SSN integer references Member(SSN),
    FID integer references  Financial_aid(FID),
    CID integer references Campaign(CID),
    primary key (SSN, FID, CID)
);
''')
cur.execute('''
    create table NCNeed (
    CID integer references Campaign(CID),
    NCID integer references  Non_cash_aid(NCID),
    primary key (CID, NCID)
);
''')


###Insertions 
cur.execute('''
    insert into charity_organization
    (coid, name, PostalCode, Address, PhoneNumber)
        values (1, 'mahak', '123456789', 'sar koche', '07132349406'),
        (2, 'mostafa','12345678', 'sar khiabon', '07138350543'),
        (3, 'hazrat Ali', '1234567', 'tehran park vey', '0218350345'),
        (4, 'mohammad', '123456', 'shiraz molasadra', '07132336402');


''')

cur.execute('''
    insert into Financial_aid 
    (fid, amount, unit, date)
        values 
        (1, 500000, 'rial', '2019-7-13'),
        (2, 23000000, 'rial', '2019-7-14'),
        (3, 1200000, 'dolar', '2019-7-15'),
        (4, 560000, 'rial', '2019-7-15'),
        (5, 3700000, 'rial', '2019-7-16'),
        (6, 500000, 'rial', '2019-7-17');

''')

cur.execute('''
    insert into Campaign 
        (cid, name, Bank_account_number, Address, Purpose, COID, GoalID)
        values
        (1, 'poyesh no', '1234-1323-1234-1234', 'shiraz kh-molasadra', 'saratan', 1, 1),
        (2, 'hamdeli', '5464-5464-5842-4578', 'khozestan kh-molasadra', 'seil', 2, 2),
        (3, 'dast pineh baste', '1234-1323-1234-1234', 'ahvaz kh-hoveize', 'kargar', 1, 2),
        (4, 'akhavi', '1223-7812-4556-1234', 'tehran kh-haft e tir', 'kodak kar', 3, 3),
        (5, 'nelson mandela', '8956-1323-4578-1234', 'shiraz kh-molasadra', 'sakht madrese', 1, 4),
        (6, 'yari', '5859-1323-1234-1234', 'kermanshah kh-molasadra', 'zelzele', 2, 6);

''')

cur.execute('''
    insert into Destitute
    (ssn, First_name , Last_name, Date_of_birth, Care_takerId, CampaignID)
        values
        (1, 'hamed', 'khazaii', '1988-2-12', 1, 1),
        (2, 'tohid', 'abedini', '1989-2-16', 2, 1),
        (3, 'keyvan', 'mirshekari', '1968-4-30', 3, 1),
        (4, 'zahra', 'abedini', '1968-6-26', 2, 2),
        (5, 'ali', 'abedini', '2000-2-23', 2, 2),
        (6, 'sara', 'kolobandi', '2004-1-13', 4, 2),
        (7, 'narges', 'kolobandi', '2001-2-24', 4, 3),
        (8, 'kamran', 'mirshekari', '2010-2-13', 3, 3);

''')

cur.execute('''
    insert into Destitute_reason 
    (SSN, Reason)
        values
        (1, 'asdlasjdlajdlaj'),
        (2, 'ksapkdaksdkasdsa'),
        (3, 'sdlaskcaspjdasjda'),
        (4, 'akscoajcoasc'),
        (5, 'bhsadasdyasgdybs'),
        (6, 'sbcuabucbsubcusanc'),
        (7, 'mcjacihasihcaishc'),
        (8, 'csabcbacasibci');

''')

cur.execute('''
    insert into Non_cash_aid
    (NCID, Value, Unit, Name, Number)
        values
        (1, 150000, 'kg', 'berenj', 12),
        (2, 230000, 'dast', 'lebas', 12),
        (3, 1200, 'kg', 'kaho', 15),
        (4, 450000, 'kg', 'kalam', 12),
        (5, 65000, 'kg', 'khiar', 13),
        (6, 450000, 'kg', 'pato', 45),
        (7, 780000, 'kg', 'balesht', 98),
        (8, 650000, 'kg', 'pirhan', 32);
''')

cur.execute('''
    insert into Member
    (SSN, User_name, First_name, Last_name, Date_of_birth, Email, Password)
        values
        (1, 'ali12', 'ali', 'mohammadi', '1988-2-12', 'alimm@gmail.com', '1231321'),
        (2, 'keyvan12', 'keyvan', 'mirshekari', '1998-4-12', 'keyvan.mih@gmail.com', '228'),
        (3, 'mohammad5643', 'mohammad', 'mohammadi', '1989-2-14', 'mohammad5643@gmail.com', '4585mmn'),
        (4, 'asfasf', 'dfsf', 'sdfsf', '1988-2-12', 'sdcsdf@gmail.com', '123dfdsf'),
        (5, 'wqeqewq', 'qweqwe', 'qewqe', '1998-2-12', 'wqeqwe@gmail.com', '12qewq321'),
        (6, 'ayiyui2', 'yuiyui', 'yiyiyu', '2000-2-12', 'yuiyuik@gmail.com', '1yuytu1'),
        (7, 'nbmnbmb', 'bnmbm', 'bnmbnm', '1898-2-12', 'mbmbnm@gmail.com', 'bnmnbm'),
        (8, 'hjkhjkh', 'jhgjhgj', 'hjhgjhg', '2008-2-12', 'hgjkhgj@gmail.com', '1ghjhgj321'),
        (9, 'etert', 'ertreter', 'erwerw', '1958-8-12', 'etert@gmail.com', '1erwerew1');
''')

cur.execute('''
    insert into Employee
    (SSN,Date_of_entry,Field,salary,COID)
        values
        (1, '2008-2-12', 'bargh', 22000000, 1),
        (3, '2009-2-12', 'mechanic', 22000000, 1),
        (7, '2012-2-12', 'riazi', 22000000, 2);
''')

cur.execute('''
    insert into Worker
    (SSN,Date_of_entry,Field,CID)
        values
        (2, '2008-2-12', 'bargh', 1),
        (5, '2009-2-12', 'mechanic', 1),
        (6, '2012-2-12', 'riazi', 2);
''')

cur.execute('''
    insert into  NCDonate 
    (SSN, NCID, CID)
        values
        (1, 1, 1),
        (2, 2, 2);
''')

cur.execute('''
    insert into FDonate 
    (SSN, FID, CID)
        values
        (3, 3, 3),
        (4, 4, 4);
''')


cur.execute('''
    insert into NCNeed 
    (CID, NCID)
        values
        (1, 1),
        (2, 1);

''')
###Triggers
cur.execute('''
CREATE FUNCTION needHandler() RETURNS TRIGGER AS $needHandler$
    DECLARE
    am  INTEGER;
    BEGIN
    am := (select financial_aid.amount FROM financial_aid NATURAL JOIN fdonate WHERE  fid=new.fid);

    UPDATE financial_aid SET amount = financial_aid.amount - am WHERE  fid=new.fid;
    END;
    $needHandler$ LANGUAGE plpgsql;

CREATE TRIGGER needHandler AFTER INSERT ON fdonate
    FOR EACH ROW
    EXECUTE PROCEDURE needHandler();

''')

cur.execute('''
CREATE FUNCTION fNeedChecker() RETURNS TRIGGER AS $fNeedChecker$
    BEGIN
    DELETE FROM financial_aid
        WHERE financial_aid.amount = 0;
    END;

    $fNeedChecker$ LANGUAGE plpgsql;

CREATE TRIGGER fNeedChecker AFTER UPDATE ON financial_aid
    FOR EACH ROW
    EXECUTE PROCEDURE fNeedChecker();
''')

cur.execute('''
CREATE FUNCTION ncNeedChecker() RETURNS TRIGGER AS $ncNeedChecker$
    BEGIN
    DELETE FROM non_cash_aid
        WHERE non_cash_aid.number = 0;
    END;

    $ncNeedChecker$ LANGUAGE plpgsql;

CREATE TRIGGER ncNeedChecker AFTER UPDATE ON non_cash_aid
    FOR EACH ROW
    EXECUTE PROCEDURE ncNeedChecker();
''')


conn.commit()
conn.close()