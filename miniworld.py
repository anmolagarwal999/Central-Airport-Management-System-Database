import subprocess as sp
import pymysql
import pymysql.cursors
import sys


from add import *
from extra import *
from read import *
from delete import *
from update import *

colors_dict = {
    "BLUE": "\033[1;34m",
    "RED": "\033[1;31m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m",
    "ERROR": "\033[;7m"+"\033[1;31m"
}


def decorate(color_str):
    # print("Decorated")
    sys.stdout.write(colors_dict[color_str])


expose_add_funcs = [["Airline", "Passenger", "Airport", "Runway", "Route", "Terminal"],
                    ["Passenger", "Aircraft", "Route",
                        "Boarding Pass", "Airline Employees"],
                    ["Feedback and rating"]]

add_funcs_dict = {
    "Airline": add_airline,
    "Passenger": add_passenger,
    "Aircraft": add_aircraft,
    "Airport": add_airport,
    "Runway": add_runway,
    "Terminal": add_terminal,
    "Route": add_route,
    "Boarding Pass": add_boarding_pass_details,
    "Airline Employees": add_airline_crew,
    "Airport Employees": add_airport_crew,
    "Feedback and rating": add_feedback
}


def add_display(cur, con, user_id):

    decorate("BLUE")
    print("Select the entity whom you would like to insert in the Database:\n")
    i = 0
    tables_add = [
        "Airline",
        "Passenger",
        "Aircraft",
        "Airport",
        "Runway",
        "Terminal",
        "Route",
        "Boarding Pass",
        "Airline Employees",
        "Airport Employees",
        "Feedback and rating"
    ]

    decorate("RED")
    for i in range(len(expose_add_funcs[user_id])):
        print(f"Press {i} for insertion in {expose_add_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_add = int(input("enter choice > "))
    if choice_to_add >= len(expose_add_funcs[user_id]) or choice_to_add < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        add_funcs_dict[expose_add_funcs[user_id][choice_to_add]](cur, con)


###########################################################################################################
expose_read_funcs = [
    ["Airline", "Passenger", "Airport", "Runway",
        "Terminal", "boarding_pass", "Route"],
    ["Route", "Airport Employees/CREWS", "Aircraft",
        "boarding_pass", "Feedback and rating"],
    ["Route", "Airline", "Airport"]
]


def read_display(cur, con, user_id):

    decorate("BLUE")
    print("Select the entity whoose entries you want to view:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_read_funcs[user_id])):
        print(f"Press {i} for reading of {expose_read_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_read = int(input("enter choice > "))
    if choice_to_read >= len(expose_read_funcs[user_id]) or choice_to_read < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        read_data(cur, con, expose_read_funcs[user_id][choice_to_read])


#################################################################################################


expose_delete_funcs = [["Airport Employees"],
                       ["Aircraft", "Route", "Airline Employees", "Luggage"],
                       []]

delete_funcs_dict = {
    # "Airline":delete_airline,#
    #  "Passenger":delete_passenger,#
    "Aircraft": delete_aircraft,
    #   "Airport":delete_airport,#
    #    "Runway":delete_runway,#
    #     "Terminal":delete_terminal,#
    "Route": delete_route,
    #      "Boarding Pass":delete_boarding_pass_details,#
    "Airline Employees": delete_airline_crew,
    "Airport Employees": delete_airport_crew,
    #       "Feedback and rating":delete_feedback,
    "Luggage": delete_luggage
}


def delete_display(cur, con, user_id):

    if user_id == 2:
        print("This user has no permissions to delete from database")
        return

    decorate("BLUE")
    print("Select the entity whose entries you want to delete:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_delete_funcs[user_id])):
        print(f"Press {i} for deletion from {expose_delete_funcs[user_id][i]}")
    decorate("RESET")

    choice_to_delete = int(input("enter choice > "))
    if choice_to_delete >= len(expose_delete_funcs[user_id]) or choice_to_delete < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        delete_funcs_dict[expose_delete_funcs[user_id]
                          [choice_to_delete]](cur, con)


#################################################################################################
#################################################################################################


expose_update_funcs = [["3", "4", "5", "6", "9"],
                       ["1", "2", "6", "7", "8"],
                       []]

update_funcs_dict = {
    "1": update_passenger,
    "2": update_aircraft,
    "3": update_airport,
    "4": update_runway_status,
    "5": update_airport_crew,
    "6": update_route_details,
    "7": update_airline_crew_personal_details,
    "8": update_airline_details,
    "9": update_atc_freq
}

update_funcs_msg = {
    "1": "for updating name, gender, address of passenger",
    "2": "for updating flight id, last check maintenance date aircraft",
    "3": "for updating name of airport",
    "4": "for updating status of runway",
    "5": "for updating name, years of experiences, salary, nationality, employer, gender of airport crew",
    "6": "for updating actual arrival time, actual departure time, distance travelled over the route, status of the journey",
    "7": "for updating airline crew personal details like salary, current employer etc.",
    "8": "for updating active_status of the airline, country of wonership",
    "9": "for updating the frequency at which the air traffic contoller is operating"
}

# in 11, give status change, time change,


def update_display(cur, con, user_id):
    if user_id == 2:
        print("This user has no permissions to update database")
        return
    decorate("BLUE")
    print("Select option as per what you want to update:\n")
    i = 0

    decorate("RED")
    # print("Decorated")
    len_use = len(expose_update_funcs[user_id])
    # print(f"len is {len_use}")
    for i in range(len_use):
        print(
            f"Press {i} for {update_funcs_msg[expose_update_funcs[user_id][i]]}")
    decorate("RESET")

    choice_to_update = int(input("enter choice > "))
    if choice_to_update >= len(expose_update_funcs[user_id]) or choice_to_update < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        update_funcs_dict[expose_update_funcs[user_id]
                          [choice_to_update]](cur, con)


#################################################################################################

expose_analysis_funcs = [["1", "2", "3", "4", "5", "6", "8", "9", "10", "11"],
                         ["1", "2", "5", "7", "8", "10", "11"],
                         ["2", "3", "5", "6", "8", "11"]]


analysis_funcs_dict = {
    "1": analysis_passenger_special_services,
    "2": analysis_big_airlines,
    "3": analysis_experienced_pilot,
    "4": analysis_search_name,
    "5": analysis_busiest_airports,
    "6": analysis_loved_airlines,
    "7": analysis_feedback_patterns,
    "8": analysis_find_tickets,
    "9": analysis_crashed_survivors,
    "10": analysis_airline_pilots,
    "11": analysis_favoured_aircrafts
}

analysis_funcs_msg = {
    "1": "Names of all passengers who have WHEELCHAIR ASSISTANCE/Disability assisstance as a special service in their BOARDING PASS",
    "2": "Names OF ALL AIRLINES whose flight crew is >=x where 'x' is to be inputted from user",
    "3": "find the pilot with maximum number of flying hrs",
    "4": "Search for all PASSENGERS whose name contains a given substring",
    "5": "RANK BUSIEST AIRPORTS by number of scheduled flight departures on a particular day",
    "6": "RANK most used airline by sorting as per the number of boarding passes issued for that airline since data collection began",
    "7": "Feedback of flight crew patterns",
    "8": "display all flights between two airports on a given date or on any date",
    "9": "names of all passengers who were travelling on a particular route/Crashed flight/Flight with a COVID infected patient",
    "10": "Names of all pilots who work for a given airline",
    "11": "Find most used aircraft across all airlines"
}


def analysis_display(cur, con, user_id):

    decorate("BLUE")
    print("Select option:\n")
    i = 0

    decorate("RED")
    for i in range(len(expose_analysis_funcs[user_id])):
        print(
            f"Press {i} for query {analysis_funcs_msg[expose_analysis_funcs[user_id][i]]}")
    decorate("RESET")

    choice_to_analysis = int(input("enter choice > "))
    if choice_to_analysis >= len(expose_analysis_funcs[user_id]) or choice_to_analysis < 0:
        print("Invalid number. Please try again\n")
        return
    else:
        analysis_funcs_dict[expose_analysis_funcs[user_id]
                            [choice_to_analysis]](cur, con)


#########################################################################################

def dispatch(ch, cur, con, user_id):
    

    if (ch == 1):
        add_display(cur, con, user_id)
    elif (ch == 2):
        update_display(cur, con, user_id)
    elif (ch == 3):
        delete_display(cur, con, user_id)
    elif (ch == 4):
        read_display(cur, con, user_id)
    elif (ch == 5):
        analysis_display(cur, con, user_id)
    else:
        print("Error: Invalid Option")


def display_menu(cur, con, user_id):

    decorate("CYAN")
    print("Select operation you want to perform")
    print("1. Add new information")
    print("2. Update tables")
    print("3. Delete data")
    print("4. Read data")
    print("5. Analysis data")
    print("6. Logout")
    decorate("RESET")

    ch = int(input("Enter choice> "))
    #tmp = sp.call('clear', shell=True)
    if ch == 6:
        raise SystemExit
    else:
        dispatch(ch, cur, con, user_id)
        tmp = input("Enter any key to CONTINUE>")


# Global
while (1):

   # Run the command described by args. Wait for command to complete, then return the returncode attribute.
    # https://stackoverflow.com/a/3172690/6427607
    tmp = sp.call('clear', shell=True)

    # Can be skipped if you want to hard core username and password
    username = input("Username: ")
    password = input("Password: ")
    # username = "root"
    # password = "blahblah"

    try:
  
        # # Connect to the database
        con = pymysql.connect(host='localhost',  # host – Host where the database server is located
                              user=username,  # Username to log in as
                              password=password,  # Password to use.
                              # Database to use, None to not use a particular one.
                              db='airport_db',
                              port=5005,  # MySQL port to use
                              cursorclass=pymysql.cursors.DictCursor)  # Custom cursor class to use.

        tmp = sp.call('clear', shell=True)

        '''Return True if the connection is open'''
        if (con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        # If you possess programming skills, you would probably use a
        #  loop like FOR or WHILE to iterate through one item at a time, do something
        #  with the data and the job is done. In T-SQL, a CURSOR
        #   is a similar approach, and might be preferred because it follows the same logic.
        decorate("CYAN")
        print("Press 0 if you are airport_employee")
        print("Press 1 if you are airline_employee")
        print("Press 2 if you are passenger")
        decorate("RESET")

        user_id = int(input())

        with con.cursor() as cur:
            while (1):
                tmp = sp.call('clear', shell=True)
                display_menu(cur, con, user_id)

    except Exception as e:
        # tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        print(">>>", e)
        tmp = input("Enter any key to CONTINUE>")
