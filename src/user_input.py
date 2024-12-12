import sys
import pandas as pd
import src.data_analysis

def select_user(viewing_records: pd.DataFrame) -> str:
    users = src.data_analysis.get_users(viewing_records)

    print("Users Found:")

    for i in range(len(users)):
        print(str(i) + ': ' + users[i])
    
    print("Select a user to analyse by entering a number, or type 'exit' to exit.")

    for i in range(5):
        number = input("User Number: ")
        if str(number).lower() == "exit":
            sys.exit(0)

        try:
            user = users[int(number)]
            break
        except:
           print("Invalid input, please try again.")
    else:
        print("Exiting due to repeated incorrect input.")
        sys.exit(0)
    
    return user

def select_media(user: str, viewing_records: pd.DataFrame) -> str:
    media_watched = src.data_analysis.get_media_for_user(viewing_records, user)

    #show_found = False
    while True:
        search_string = input("\nEnter a string to look for media with matching name:\n")
        matching_media = []
        for i in media_watched:
            if search_string.lower() in str(i).lower():
                matching_media.append(i)

        #print("length: " + str(len(matching_media)))

        if len(matching_media) == 0:
            print("\nNo results found, please try again.")
            continue

        if len(matching_media) == 1:
            show_found = True
            return str(matching_media[0])

        if len(matching_media) <= 10:
            print("\nFound " + str(len(matching_media)) + " results:")

            for i in range(len(matching_media)):
                print(str(i) + ": " + str(matching_media[i]))
            print("Please select a results using a number, or type 'exit' to exit.")
            print("Anything else will reset search.")
            user_input = input()
            if str(user_input).lower() == 'exit':
                sys.exit(0)
            try:
                return str(matching_media[int(user_input)])
            except:
                print("Invalid input, resetting search.")
                continue
        
        print("-- Too many results found, please enter something more specific. --")
            
