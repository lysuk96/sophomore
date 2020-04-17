import pymysql as pms

host = 'localhost'
port = 3306
user = 'root'
psw = 'gkqrur236!'
charset = 'utf8'
db = 'melon'

connection = pms.connect(host, user, psw, db, port, charset = charset)
cursor = connection.cursor()
global id

def execute_commit(sql) :
    cursor.execute(sql)
    connection.commit()
    return

def execute_commit_data(sql, data):
    cursor.execute(sql, data)
    connection.commit()
    return

def check(sql) :
    cursor.execute(sql)
    check = cursor.fetchone()
    return check

def print_all(sql) :
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)) :
        print(i+1, ": ", result[i])
    return

def print_all_data(sql,data) :
    cursor.execute(sql,data)
    result = cursor.fetchall()
    for i in range(len(result)) :
        print(i+1, ": ", result[i])
    return


if __name__ == "__main__" :
    status = 1
    print("Select Mode")
    print("0. Administrator Mode")
    print("1. User Mode")
    mode = int(input('Input : '))
    crt = -1 #certification

    if (mode == 0) :
        while 1:
            print("\nInsert Admin ID")
            id = input('Admin ID : ') #root id = 11111
            sql = "SELECT * FROM `administrator` WHERE Id = '{}'".format(id)
            if check(sql) :
                crt = 0
                break
            else : print("Wrong!!! Do it again")
    elif (mode == 1) :
        while 1:
            print("Insert User ID")
            id = input ('User ID : ')
            sql = "SELECT * FROM `user` WHERE Id = '{}'".format(id)
            if check(sql) :
                crt = 1
                break
            else : print("Wrong!!! Do it again")

    while (status == 1 and crt == 0) : #Status 1, Administrator Mode
        print("\n0. Exit")
        print("1. Administrator Menu")
        print("2. User Menu")
        print("3. Music Menu")
        first = int(input('Input : '))

        if(first == 0) :
            status -= 1
        elif(first == 1) :
            status += 1
            while(status >= 2): #Status 2
                print("\n0. Return to previous menu")
                print("1. Register new Administrator")
                print("2. View all Administrators")
                print("3. View attributes")
                second = int(input('Input : '))
                if(second == 0) : #Status 3
                    status -= 1
                elif(second == 1) : #Status = 3
                    while (1) :
                        name = input('\nName : ')
                        new_id = input('ID, should be 5 numbers :')
                        sql = "SELECT * FROM `administrator` WHERE Id = '{}'".format(new_id)
                        if check(sql) : print("ID already exists. Insert other ID!")
                        else :
                            sql = "INSERT INTO `administrator` (`Name`, Id) VALUE ('{}', '{}')".format(name, new_id)
                            execute_commit(sql)
                            break
                elif(second == 2) : #Status 3
                    #Admin 모두 보여주고 delete, update 진행
                    while 1:
                        sql = "select * from `administrator`"
                        print("\n------------------------------\nIndex : (ID, Name, Sex, Address, Phone_no, Mgr_id)\n------------------------------\n")
                        print_all(sql)
                        print("\n------------------------------\n")
                        print("\n0. Return to previous menu")
                        print("1. Delete Administrator")
                        print("2. Update Administrator")
                        third = int(input('Input : '))
                        if (third == 0):
                            break
                        elif (third == 1):
                            delete_id = input('Write the Admin id you want to Delete : ')
                            sql = "delete from `administrator` where Id = '{}'".format(delete_id)
                            execute_commit(sql)
                        elif (third == 2):
                            while 1 :
                                update_id = input('\nWrite the Admin id you want to Update : ')
                                sql = "SELECT * FROM `administrator` WHERE Id = '{}'".format(update_id)
                                if (check(sql)) : break
                                else : 
                                    flag = input('Check the id Again. Want to try again?(y/n) : ')
                                    if (flag == 'n'): break
                            if(flag == 'n'): break
                            while 1:
                                name = input('Name : ')
                                if name == '': print("Name should not be Nonetype")
                                else : break
                            sex = input('Sex(f/m) : ')
                            if sex == '' : sex =None
                            address = input('Address : ')
                            if address == '': address =None
                            phone_no = input('Phone Number : ')
                            if phone_no == '' : phone_no = None
                            mgr_id = input('Manager ID : ')
                            if mgr_id == '' : mgr_id = None                       
                            sql = "update administrator set Name= %s, Sex= %s, Address= %s, Phone_no= %s, Mgr_id = %s where Id = {}".format(update_id)
                            data = (name, sex, address, phone_no, mgr_id)
                            execute_commit_data(sql, data)
                elif (second == 3) : #Status 3
                    #atribute 출력하고 거기에 해당하는 attribute 선택 후 출력
                    print("1.Id\t2.Name\t3.Sex\t4.Address\t5.Phone_no\t6.Mgr_id")  
                    flag = int(input('Which attribute do you want to see?\nType the right number : '))
                    if flag == 1: sql = "select Id from `administrator`"
                    elif flag == 2: sql = "select distinct Name from `administrator`"
                    elif flag == 3: sql = "select distinct Sex, count(*) from `administrator` group by Sex"
                    elif flag == 4: sql = "select distinct Address from `administrator`"
                    elif flag == 5: sql = "select distinct Phone_no from `administrator`"
                    elif flag == 6: sql = "select distinct Mgr_id from `administrator`"
                    print_all(sql)
        elif (first == 2) :
            status += 1
            while(status >= 2) : #Status 2
                print("\n0. Return to previous menu")
                print("1. Register new User")
                print("2. View All Users")
                print("3. View attributes")
                second = int(input('Input : '))
                if(second == 0) :
                    status -= 1
                elif (second == 1) :
                    while (1) :
                        name = input('\nName : ')
                        new_id = input('ID, should be 5 numbers :')
                        sql = "SELECT * FROM `user` WHERE Id = '{}'".format(new_id)
                        if check(sql) : print("ID already exists. Insert other ID!")
                        else :
                            sql = "INSERT INTO `user` (`Name`, Id, Ad_id) VALUE ('{}', '{}', '{}')".format(name, new_id, id)
                            execute_commit(sql)
                            sql = "Insert into `playlist` (Usr_id) value ('{}')".format(new_id)
                            execute_commit(sql)
                            break
                elif (second == 2) :
                    #User 모두 보여주고 delete, update, ban진행
                    while 1:
                        sql = "select * from `user`"
                        print("\n------------------------------\nIndex : (ID, Name, Sex, Coin, Address, Phone_no, Ad_id, Banned)\n------------------------------\n")
                        print_all(sql)
                        print("\n------------------------------\n")
                        print("\n0. Return to previous menu")
                        print("1. Delete User")
                        print("2. Update User")
                        print("3. Ban User")
                        print("4. Permit User ")
                        third = int(input('Input : '))
                        if third == 0 :break
                        elif (third == 1):
                            delete_id = input('Write the User id you want to Delete : ')
                            sql = "delete from `add_on` where Usr_id = '{}'".format(delete_id)
                            execute_commit(sql)
                            sql = "delete from `playlist` where Usr_id = '{}'".format(delete_id)
                            execute_commit(sql)
                            sql = "delete from `user` where Id = '{}'".format(delete_id)
                            execute_commit(sql)
                        elif (third == 2):
                            while 1 :
                                update_id = input('\nWrite the User id you want to Update : ')
                                sql = "SELECT * FROM `User` WHERE Id = '{}'".format(update_id)
                                if (check(sql)) : break
                                else : 
                                    flag = input('Check the id Again. Want to try again?(y/n) : ')
                                    if (flag == 'n'): break
                            if(flag == 'n'): break
                            while 1:
                                name = input('Name : ')
                                if name == '': print("Name should not be None")
                                else : break
                            sex = input('Sex(f/m) : ')
                            if sex == '' : sex =None
                            coin = input('Coin : ')
                            if coin == '' : coin = 0
                            else : coin = int(coin)
                            address = input('Address : ')
                            if address == '': address =None
                            phone_no = input('Phone Number : ')
                            if phone_no == '' : phone_no = None
                            ad_id = input('Administrator ID : ')
                            if ad_id == '' : ad_id = None           
                            sql = "update user set Name= %s, Sex= %s, Coin = %s, Address= %s, Phone_no= %s, Ad_id = %s where Id = {}".format(update_id)
                            data = (name, sex, coin, address, phone_no, ad_id)
                            execute_commit_data(sql,data)
                        elif (third == 3) :
                            ban_id = input('Write the User id you want to ban : ')
                            sql = "update user set banned = True where Id = '{}'".format(ban_id)
                            execute_commit(sql)
                        elif (third == 4) :
                            permit_id = input('Write the User id you want to permit : ')
                            sql = "update user set banned = False where Id = '{}'".format(permit_id)
                            execute_commit(sql)
                elif(second == 3) :
                    #attribute 출력하고 거기 해당하는 attribute 선택 후 출력
                    print("1.Id\t2.Name\t3.Sex\t4.Coin\t5.Address\t6.Phone_no\t7.Ad_id")    
                    flag = int(input('Which attribute do you want to see?\nType the right number : '))
                    if flag == 1: sql = "select Id from `user`"
                    elif flag == 2: sql = "select distinct Name from `user`"
                    elif flag == 3: sql = "select distinct Sex, count(*) from `user` group by Sex"
                    elif flag == 4: sql = "select distinct Coin from `user`"
                    elif flag == 5: sql = "select distinct Address from `user`"
                    elif flag == 6: sql = "select distinct Phone_no from `user`"
                    elif flag == 7: sql = "select distinct Ad_id, count(*) from `user`  group by Ad_id"
                    print_all(sql)
        elif (first == 3) :
            status += 1
            while(status >= 2) : #Status 2
                print("\n0. Return to previous menu")
                print("1. Insert new music")
                print("2. View all musics")
                print("3. View attributes")
                second = int(input('Input : '))
                if (second == 0):
                    status -= 1
                elif (second == 1):
                    while (1) :
                        title = input('Title : ')
                        new_id = input('ID, should be 5 numbers :')
                        sql = "SELECT * FROM `music` WHERE Id = '{}'".format(id)
                        if check(sql) : print("ID already exists. Insert other ID!")
                        else :
                            sql = "INSERT INTO `music` (`Title`, Id) VALUE ('{}', '{}')".format(title, new_id)
                            execute_commit(sql)
                            break
                elif (second == 2) :
                    #Music 모두 보여주고 delete, update 진행
                     while 1:
                        sql = "select * from `music`"
                        print("\n------------------------------\nIndex : (ID, Title, Artist, Composer, Lyricist, Ad_id)\n------------------------------\n")
                        print_all(sql)
                        print("\n------------------------------\n")
                        print("\n0. Return to previous menu")
                        print("1. Delete Music")
                        print("2. Update Music")
                        third = int(input('Input : '))
                        if third == 0 :break
                        elif (third == 1):
                            delete_id = input('Write the Music id you want to Delete : ')
                            sql = "delete from `music` where Id = '{}'".format(delete_id)
                            execute_commit(sql)
                        elif (third == 2):
                            while 1 :
                                update_id = input('\nWrite the Music id you want to Update : ')
                                sql = "SELECT * FROM `music` WHERE Id = '{}'".format(update_id)
                                if (check(sql)) : break
                                else : 
                                    flag = input('Check the id Again. Want to try again?(y/n) : ')
                                    if (flag == 'n'): break
                            while 1:
                                title = input('Title : ')
                                if title == '': print("Title should not be None")
                                else : break  
                            artist = input('Artist : ')
                            if artist == '': artist = None
                            composer = input('Composer : ')
                            if composer == '': composer = None
                            lyricist = input('Lyricist : ')
                            if lyricist == '': lyricist = None
                            sql = "alter table music drop Foreign key music_ibfk_1"
                            execute_commit(sql)
                            sql = "update music set Title = %s, Artist = %s, Composer = %s, Lyricist = %s, Ad_id = %s where Id = '{}'".format(update_id)
                            data = (title, artist, composer, lyricist, id)
                            execute_commit_data(sql, data)
                            sql = "alter table music add foreign key (Ad_id) references Administrator(id)"
                            execute_commit(sql)
                elif (second == 3) :
                    #attribute 출력하고 거기 해당하는 attribute 선택 후 출력
                    print("1.Id\t2.Title\t3.Artist\t4.Composer\t5.Lyricist\t6.Ad_id")    
                    flag = int(input('Which attribute do you want to see?\nType the right number : '))
                    if flag == 1: sql = "select Id from `music`"
                    elif flag == 2: sql = "select distinct Title from `music`"
                    elif flag == 3: sql = "select distinct Artist, count(*) from `music` group by Artist"
                    elif flag == 4: sql = "select distinct Composer, count(*) from `music` group by Composer"
                    elif flag == 5: sql = "select distinct Lyricist, count(*) from `music` group by Lyricist"
                    elif flag == 6: sql = "select distinct Ad_id, count(*) from `music`  group by Ad_id"
                    print_all(sql)

    while(status == 1 and crt == 1) : #Status1, User Mode
        print("\n0. Exit")
        print("1. Show My Playlist")
        print("2. Insert Music on The Playlist")
        print("3. Delete Music on The Playlist")
        print("4. Buy the coins")
        print("5. Show my data")
        first = int(input('Input : '))
        if(first == 0):
            status -= 1
        elif(first == 1):
            #playlist와 음악 모두 보여주기
            print("\n------------------------------\nIndex : (Id, Title, Artist, Composer, Lyricist)\n------------------------------\n")
            sql = "select Id, Title, Artist, Composer, Lyricist from `music`, `add_on` where Id = Msc_id and Usr_id = '{}'".format(id)
            print_all(sql)
            print("\n------------------------------\n")
        elif(first == 2):
            #insert, coin 세개 써서 사기, 남은 코인 보여주기
            sql = "select banned from `user` where Id = '{}'".format(id)
            cursor.execute(sql)
            result = bool(cursor.fetchone()[0])
            if result is True : print("You are BANNED! You are not allowed to insert into Playlist!")
            else :
                sql = "select Coin from `user` where Id = '{}'".format(id)
                cursor.execute(sql)
                result = int(cursor.fetchone()[0])
                if result < 3 : print("Your coins are not enough")
                else :
                    result -= 3
                    choice = int(input('1.Show All\t2. Search by the Title : '))
                    if choice == 1: #Show All
                        sql = "select ID, Title, Artist, Composer, Lyricist from `music`"
                        print("\n------------------------------\nIndex : (ID, Title, Artist, Composer, Lyricist)\n------------------------------\n")
                        print_all(sql)
                        print("\n------------------------------\n")
                        flag = input('Which one do you want to add?\nID : ')
                        sql = "INSERT INTO `add_on` (`Msc_id`, Usr_id) VALUE ('{}', '{}')".format(flag, id)
                    elif choice == 2: #Search by the Title
                        flag = input('Which one do you want to add?\nTitle : ')
                        flag = '%' + flag + '%'
                        sql = "select ID, Title, Artist, Composer, Lyricist from `music` where Title Like %s"
                        print("\n------------------------------\nIndex : (ID, Title, Artist, Composer, Lyricist)\n------------------------------\n")
                        print_all_data(sql,flag)
                        print("\n------------------------------\n")
                        flag = input('Which one do you want to add?\nID : ')
                        sql = "INSERT INTO `add_on` (`Msc_id`, Usr_id) VALUE ('{}', '{}')".format(flag, id)
                    execute_commit(sql)
                    sql = "update user set coin = %s where Id = '{}'".format(id)
                    execute_commit_data(sql, result)
        elif(first == 3):
            #delete
            sql = "select banned from `user` where Id = '{}'".format(id)
            cursor.execute(sql)
            result = bool(cursor.fetchone()[0])
            if result is True : print("You are BANNED! You are not allowed to delete music!")
            else :
                flag = input('Which one do you want to delete?\nID : ')
                sql = "delete from add_on where Msc_id = '{}'".format(flag)
                execute_commit(sql)
                print("Delete Complete")
        elif(first == 4):
            #coin 사기
            coin = int(input('How much money do you pay?(/won) : ')) // 100
            print("Complete! You earned " + str(coin) + " coins")
            sql = "update user set Coin = Coin + %s where ID = '{}'".format(id)
            data = (coin)
            execute_commit_data(sql, data)
        elif(first == 5) :
            #show my data
            sql = "select * from `user` where Id = '{}'".format(id)
            print("\n------------------------------\nIndex : (ID, Name, Sex, Coin, Address, Phone_no, Ad_id, Banned)\n------------------------------\n")
            print_all(sql)
            print("\n------------------------------\n")
            flag = input('Want to update? (y/n) : ')
            if (flag == 'y'):
                while 1:
                    name = input('Name : ')
                    if name == '': print("Name should not be None")
                    else : break
                sex = input('Sex(f/m) : ')
                if sex == '' : sex =None
                address = input('Address : ')
                if address == '': address =None
                phone_no = input('Phone Number : ')
                if phone_no == '' : phone_no = None      
                sql = "update user set Name= %s, Sex= %s, Address= %s, Phone_no= %s where Id = {}".format(id)
                data = (name, sex, address, phone_no)
                execute_commit_data(sql,data)
                print("Update Complete")

