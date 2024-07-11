#FlightExplorer

#modules
import mysql.connector 
from tabulate import tabulate

#functions
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cathycerine101",
            database="tickets"
        )
        if connection.is_connected():
            print()
            print("Welcome to Flight Explorer!")
            print()
            print('▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝')
            print()
            return connection
    except Exception as e:
        print("Error", e)
        return None
    
flight_ids_list = []

def show_available_flights(connection, user_month, user_departure, user_destination):
    try:
        cursor = connection.cursor()

        #available flights based on user input
        query =  """
            SELECT af.flight_id, af.departure_date, fd.departure_time, fd.arrival_time, fd.airline
            FROM available_flights af
            LEFT JOIN flight_details fd ON af.flight_id = fd.flight_id
            WHERE af.departure_city = %s AND af.destination_city = %s AND af.departure_month = %s
        """

        values = (user_departure, user_destination, user_month)

        cursor.execute(query, values)

        rows = cursor.fetchall()

        if not rows:
            return False
        else:
            #available flights table
            print(f"Available flights from {user_departure} to {user_destination} on {user_month} :")
            
            headers = ["S_No", "Flight Number","Date", "Departure Time", "Arrival Time","Airline"]
            data = [(i + 1, row[0], row[1], row[2], row[3], row[4]) for i, row in enumerate(rows)]
            print(tabulate(data, headers=headers, tablefmt="pretty"))
            
            flight_ids_list.extend([row[0] for row in rows]) #add flight ids to list
            return True
            
    except Exception as e:
        print("Error", e)
    finally:
        cursor.close()
        
def check_seats_availability(connection, flight_id, no_passengers):
    try:
        cursor = connection.cursor()

        #available seats 
        query = "SELECT seats FROM flight_details WHERE flight_id = %s"
        cursor.execute(query, [flight_id])
        available_seats = cursor.fetchone()

        if available_seats is not None:
            available_seats = int(available_seats[0])

            if available_seats >= no_passengers:               
                return True
            else:
                return False
        else:
            print("Error")

    except Exception as e:
        print("Error", e)
    finally:
        cursor.close()
    
def update_seats_after_payment(connection, flight_id, no_passengers):
    try:
        cursor = connection.cursor()

        #update the seats after payment
        query_update = "UPDATE flight_details SET seats = seats - %s WHERE flight_id = %s"
        cursor.execute(query_update, (no_passengers, flight_id))
        connection.commit()

        print("Your payment was succesful!!")
        print()
        print('Thank you for using Flight Explorer!')
        print('▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝')

    except Exception as e:
        print(e)
    finally:
        cursor.close()

def get_flight_details(connection, flight_id):
    try:
        cursor = connection.cursor()
        
        query = """
            SELECT af.departure_date, fd.departure_time, fd.arrival_time, fd.airline
            FROM available_flights af
            LEFT JOIN flight_details fd ON af.flight_id = fd.flight_id
            WHERE af.flight_id = %s
        """

        cursor.execute(query, (flight_id,))
        flight_details = cursor.fetchone()

        if flight_details:
            departure_date, departure_time, arrival_time, airline = flight_details
            return airline, departure_date, departure_time, arrival_time
        else:            
            return None

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        
#main program
connection = connect_to_mysql()

destination_AUH = [('India', 'Trivandrum', 'Madras', 'Goa', 'Bombay', 'Kolkata', 'Dehli'),
                   ('Saudi Arabia', 'Riyadh', 'Jeddah'),
                   ('Egypt', 'Giza', 'Cairo'),
                   ('United Kingdom', 'London', 'Birmingham')]

destination_DXB = [('India', 'Trivandrum', 'Madras,Bombay', 'Hyderabad', 'Kolkata'),
                   ('Saudi Arabia', 'Riyadh', 'Jeddah'),
                   ('Egypt', 'Alexandria', 'Cairo', 'Giza'),
                   ('United Kingdom', 'London', 'Birmingham', 'Manchester', 'Glasgow')]

city = ('Dubai', 'Abu Dhabi')
non_veg_meals = ['Butter chicken and naan','Chicken and Egg sandwich','Chicken salad','Bacon and Eggs','Spicy Lamb curry','Chicken Tikka masala','Chicken soup','Beef lasgna','Chicken pasta']
veg_meals = ['Salad.']
departure_city = {1: destination_DXB,
                  2: destination_AUH}

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']

print('1. Book a flight')
print('2. Exit')
user_option = input('- ')
   
while user_option != '1' and user_option != '2' :
    print()
    print('Invalid option, please enter again!')  
    print()
    print('1. Book a flight')
    print('2. Exit')
    user_option = input('- ')

if user_option == '1':
    print()
    print('Choose departure city ')
    print('1. Dubai')
    print('2. Abu Dhabi')
    user_dp = input('- ')
        
    while user_dp != '1' and user_dp != '2' :
        print()
        print('Invalid option, please enter again!')  
        print()
        print('1. Dubai')
        print('2. Abu Dhabi')
        user_dp = input('- ')
    user_dp = int(user_dp)    
    user_departure = city[user_dp - 1]  
    print()
    print('1. view destinations')
    print('2. Cancel')
    user_option = input('- ')
    print()
                
    while user_option != '1' and user_option != '2' :
        print()
        print('Invalid option, please enter again!')
        print()
        print('1. view destinations')
        print('2. Cancel')
        user_option = input('- ')
        print()
    
    if user_option == '1':                
        print('Select destination country ')
        destinations = departure_city[user_dp]
        option_list = []
        s_no = 1
        for i in range(len(destinations)):
            option_list +=[s_no]
            print(s_no, '.', sep='', end=' ')
            print(destinations[i][0])
            s_no += 1
        user_option = input('- ') 
        
        while True :            
            if user_option.isnumeric():  
                user_option = int(user_option)
                
                if int(user_option) in option_list :
                    print()
                    user_country = destinations[user_option - 1][0]  #selected country
                    print()
                    print('[ Selected country :',user_country,']')
                    selected_city = destinations[user_option - 1]
                    print()
                    break
                else :
                    print()
                    print('Invalid option!')  
                    user_option = input('- ')
                    print()                      
        else :
            print('Invalid option!')
            user_option = input('- ')
                                        
        user_option = int(user_option)
               
        print('Select destination city')
        option_list = []
        s_no = 1
        
        for i in destinations[user_option - 1]:
            option_list += [s_no]
            if i == destinations[user_option - 1][0]:
                continue
            else:
                print(s_no, '.', sep='', end=' ')
                print(i)
                s_no += 1
                
        user_option = input('- ')           
        while True :
            
            if user_option.isnumeric():  
                user_option = int(user_option)
                
                if int(user_option) in option_list :
                    print()
                    user_city = selected_city[user_option] #selected city
                    print('[ Selected city :',user_city,']') 
                    print()
                    break
                else :
                    print()
                    print('Invalid option!')  
                    user_option = input('- ')
                    print()                      
        else :
            print('Invalid option!')
            user_option = input('- ')

        print('Select month')
        s_no = 1
        option_list = []
        for i in months:
            option_list += [s_no]
            print(s_no, '.', sep='', end=' ')
            print(i)
            s_no += 1
        user_option = int(input('- '))
        
        while user_option not in option_list :
            print()
            print('Invalid option, please enter again!')
            print()
            user_option = int(input('- '))
                    
        user_month = months[user_option - 1]  #selected month
        print('[ Selected month :',user_month,']')
        print()
        print('1. View Available flights')
        print('2. Exit ')
        user_option = input('- ')
        print()
                  
        while user_option != '1' and user_option != '2' :
            print()
            print('Invalid option, please enter again!')
            print()
            print('1. view Available flights')
            print('2. Exit')
            user_option = input('- ')
            print()
        user_option = int(user_option)
        
        flights = show_available_flights(connection, user_month, user_departure, user_city) 
        while flights is False :
            print()
            print(f'No available flights from {user_departure} to {user_city} on {user_month} :( ')
            print()
            print('Would you like to select another month?')
            print()
            print('1. Yes')
            print('2. No')
            user_option = input('- ')
            while user_option != '1' and user_option != '2' :
                print()
                print('Invalid option, please enter again.')
                print()  
                user_option = input('- ')                  
            user_option = int(user_option)    
                
            if user_option == 1 : 
                                                                   
                print('Select month')
                s_no = 1
                option_list = []
                for i in months:
                    option_list += [s_no]
                    print(s_no, '.', sep='', end=' ')
                    print(i)
                    s_no += 1
                user_option = input('- ')
                while user_option.isnumeric() == False :
                    print('Invalid option, please enter a number!')
                    user_option = input('- ')
                user_option = int(user_option)       
                while user_option not in option_list :
                    print()
                    print('Invalid month, please enter a number between 1-12!')
                    print()
                    user_option = int(input('- '))
                            
                user_month = months[user_option - 1]
                print()
                print('1. View Available flights')
                print('2. Exit ')
                user_option = int(input('- '))
                print()
                        
                while user_option != 1 and user_option != 2 :
                    print()
                    print('Invalid option, please enter again!')
                    print()
                    print('1. view Available flights')
                    print('2. Exit')
                        
                    user_option = int(input('- '))
                    print()
                                                                
                else :
                    break
                                                
        if user_option == 1:  
            
            print('Select flight')
            user_option = int(input('- '))
            user_flight_id = flight_ids_list[user_option-1]
            print()
        
            print('Enter number of passengers ')
            no_passengers = int(input('- '))            
            available = check_seats_availability(connection, user_flight_id, no_passengers)
        
            while available is False:
                print()
                print(f'Not enough seats for {no_passengers} passengers :(')
                print()
                print('Would you like to select another flight?')
                print('1. Yes')
                print('2. No')
                user_option = input('- ')
                print()
                
                while user_option.isnumeric() == False :
                    print('Please enter a number!')
                    user_option = input('- ')
                    print()
                user_option = int(user_option)
                
                while user_option != 1 and user_option != 2:
                    print('Invalid option!')
                    user_option = int(input('- '))
                    print()
        
                if user_option == 1:
                    show_available_flights(connection, user_month, user_departure, user_city)
                    print('Select flight')
                    user_option = int(input('- '))
                    user_flight_id = flight_ids_list[user_option-1]
                    print()              
                    print('Enter number of passengers ')
                    no_passengers = int(input('- '))
                    available = check_seats_availability(connection, user_flight_id, no_passengers)
                
            passenger_list = {}  #passenger names with details
            price = 0
                        
            for i in range(no_passengers) :
                
                print()
                class_price = 0
                discount = 1
                passenger_details = [] #dob, class, meal
                print('Enter name of passenger',i+1)
                passenger_name = input('- ')
                print()
                print('Enter Date of birth')
                print()
                print('Year :')
                year = int(input('- '))
                while year < 1940 :
                    print('Please enter correct year ')
                    year = int(input('- '))
                                        
                print('Month :')
                month = input('- ')
                print('Day :')
                day = input('- ')
                bday = '.'.join([str(year),month,day])
                passenger_details += [bday]
                print() 
                
                # other passenger details
                print('Enter passport number')
                passport_no = input('- ')
                print()
                
                while len(passport_no) != 12 :
                    print('Invalid passport number, please try again')
                    passport_no = input('- ')
                    print()
                
                print('Date of expiry' )
                print('[YY.MM.DD]')
                a = input('- ')
                print()
                print('Enter nationality')
                user_nationality = input('- ')
                print()
                                
                #ticket price  
                if 2024 - year < 12 :   #50% discount for children under 12
                    discount = 50/100   
                
                print('Select class')
                print('1. Buisiness CLass')  #B
                print('2. Economy Class')    #E
                print('3. First Class')      #F
                user_option = input('- ')
                                                                     
                while user_option not in ['1','2','3'] :
                    print('Please enter 1,2,or 3')
                    user_option = input('- ')
                user_option = int(user_option)
                
                if user_option == 1 :
                    passenger_details += ['Buisiness']
                    price += 500 * discount
                    class_price = 500
                elif user_option == 3 :
                    passenger_details += ['First Class']
                    price += 800 * discount
                    class_price = 800
                else :
                    passenger_details += ['Economy']
                    price += 300 * discount
                    class_price = 300
                    
                if 2024 - int(year) < 10 :
                    price += price * 20/100
                elif 2024 - int(year) >= 60 :
                    price += price * 35/100
                else :
                    price += price
                               
                print('Select meal type :')
                print('1. Veg')
                print('2. Non-veg')
                user_option = input('- ')      
                while user_option != '1' and user_option != '2' :
                    print('Invalid option, please try again')
                    user_option = input('- ')
                user_option = int(user_option)
                s_no = 1
                option_list = []
                if user_option == 1 :
                    print('Select meal')
                    for i in veg_meals :
                        option_list += [s_no]
                        print(s_no,'.',sep='',end=' ')
                        print(i)
                        s_no += 1
                    user_option = int(input('- ')) 
                    while user_option not in option_list :
                        print('Invalid option, please enter again!')
                        user_option = int(input('- '))
                    user_meal = veg_meals[user_option-1]
                    print('[ Selected meal:',user_meal,']')                
                     
                elif user_option == 2 :
                    print('Select meal')
                    for i in non_veg_meals :
                        option_list += [s_no]
                        print(s_no,'.',sep='',end=' ')
                        print(i)
                        s_no += 1
                    user_option = int(input('- '))
                    while user_option not in option_list :
                        print('Invalid option, please enter again!')
                        user_option = int(input('- '))
                    user_meal = non_veg_meals[user_option-1]
                    print('[ Selected meal:',user_meal,']')  
      
                passenger_details += [user_meal]   
                passenger_details += [class_price]
                passenger_details += [discount]
                passenger_list[passenger_name] = passenger_details            
                del passenger_details
                
            #contact details   
            print('Enter email address')
            user_email = input('- ')
            print()
            while '@' not in user_email and '.' not in user_email :
                print('Please enter valid email address!')
                user_email = input('- ')
                print()
            print('Enter mobile number')
            user_mno = int(input('- '))
            print()           
            while len(str(user_mno)) != 10 :
                print('PLEASE enter valid number!')
                user_mno = int(input('- '))
                print()           
                        
            #confirmation                                                                            
            print('Total amount :',end=' ')        
            print('AED',price)    
            print('1. Trip Summary')
            print('2. Book ticket')
            print('3. Cancel')
            print()
            user_option = int(input('-'))
            
            if user_option == 2 :      
                print('Enter credit card number')
                credit_card = int(input('- '))
                print()   
                while len(str(credit_card)) != 12 : 
                    print('Invalid number, please enter again')
                    credit_card = input('- ')
                    print()   
                update_seats_after_payment(connection, user_flight_id, no_passengers)
                                        
            if user_option == 1 :             
                flight_info = get_flight_details(connection, user_flight_id)
                if flight_info:  
                   #unpacking 
                    airline, departure_date, departure_time, arrival_time = flight_info         
                    print()
                    print('Trip Summary')
                    print()
                    print('▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝')
                    print()
                    print('From:', user_departure)
                    print('To:', user_city)
                    print('Date:',departure_date)
                    print('Airline:', airline) 
                    print('Departure time:',departure_time)
                    print('Arrival time:',arrival_time)
                    print('Flight ID:', user_flight_id)
                    print('Number of passengers:', no_passengers)

                    for i in passenger_list:  
                        print()
                        print('Name:', i)
                        print('Class type:', passenger_list[i][1], end=' ')
                        print('[ AED', passenger_list[i][3], ']')
                        print('Meal:', passenger_list[i][2])
                        if passenger_list[i][4] == 1 :
                            continue
                        else :
                            print('Available Discount : 50% off for kids below 12')
                    print('Total amount: AED',price)
                    print()
                    print('▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝')
                    print()
                print('1. Book ticket')
                print('2. Cancel')                
                user_option = int(input('- '))
                print()
                
                if user_option ==1 :                
                    print('Enter credit card number')
                    credit_card = int(input('- '))
                    print()     
                    while len(str(credit_card)) != 16 : 
                        print('Invalid number, please enter again')
                        credit_card = input('- ')  
                    update_seats_after_payment(connection, user_flight_id, no_passengers)
                                    
else :
    print()
    print('Exiting....')    
    print()
    print('▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝▝')
               
