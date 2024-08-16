import telepot
from telepot.loop import MessageLoop
import pandas as pd

# Load the Excel data into DataFrames
excel_file_path_1 = 'C:\\Users\\amark\\Downloads\\CSE.xlsx'
excel_file_path_2 = 'C:\\Users\\amark\\Downloads\\CSEIII22.xlsx'
excel_file_path_3 = 'C:\\Users\\amark\\Downloads\\SEM720.xlsx'
excel_file_path_4 = 'C:\\Users\\amark\\Downloads\\SEMV21.xlsx'
excel_file_path_5 = 'C:\\Users\\amark\\Downloads\\CSE20208.csv'
excel_file_path_6 = 'C:\\Users\\amark\\Downloads\\CSE20216.csv'
df_cse20214 = pd.read_excel(excel_file_path_1).fillna(' ')
df_cse20215 = pd.read_excel(excel_file_path_4).fillna(' ')
df_cse20216 = pd.read_csv(excel_file_path_6).fillna(' ')
df_cse20223 = pd.read_excel(excel_file_path_2).fillna(' ')
df_cse20207 = pd.read_excel(excel_file_path_3).fillna(' ')
df_cse20208 = pd.read_csv(excel_file_path_5).fillna(' ')


# Dictionary to keep track of user states
user_states = {}

# Function to handle incoming messages
def handle_message(msg):
    chat_id = msg['chat']['id']
    user_input = msg['text'].strip()

    # Initialize user state if not already present
    if chat_id not in user_states:
        user_states[chat_id] = {'state': 'START'}

    user_state = user_states[chat_id]['state']

    # Define helper functions
    def ask_student_id():
        bot.sendMessage(chat_id, "Please enter your Student ID:")

    def ask_semester():
        bot.sendMessage(chat_id, "Please enter the semester (e.g., '3' for 3rd semester):")

    def send_student_data(student_data, batch_no, semester_no):
        if not student_data.empty:
            data_message = f"SEMESTER_NO: {semester_no}\nBATCH_NO: {batch_no}\n"
            data_message += f"Student ID: {student_data['Student_id'].values[0]}\n"
            for column in student_data.columns:
                if column != 'Student_id':
                    data_message += f"{column}: {student_data[column].values[0]}\n"
            bot.sendMessage(chat_id, data_message)
        else:
            bot.sendMessage(chat_id, f"Student with ID {user_states[chat_id]['student_id']} not found.")

    # Handle different states
    if user_state == 'START':
        ask_student_id()
        user_states[chat_id]['state'] = 'AWAITING_STUDENT_ID'

    elif user_state == 'AWAITING_STUDENT_ID':
        user_states[chat_id]['student_id'] = user_input
        ask_semester()
        user_states[chat_id]['state'] = 'AWAITING_SEMESTER'

    elif user_state == 'AWAITING_SEMESTER':
        student_id = user_states[chat_id]['student_id']
        semester_no = user_input.upper()
        user_states[chat_id]['state'] = 'START'

        # Identify the batch and type (regular or lateral) based on student ID
        if student_id[1] == "1" and student_id[4] != '5':
            # Regular student in batch 2021
            if semester_no == '4':
                student_data = df_cse20214[df_cse20214['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            elif semester_no == '5':
                student_data = df_cse20215[df_cse20215['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            elif semester_no=='6':
                student_data = df_cse20216[df_cse20216['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            #elif semester_no=='7':
             #   student_data = df_cse20214[df_cse20214['Student_id'] == student_id]
              #  send_student_data(student_data, batch_no="2021", semester_no=semester_no)    
            else:
                bot.sendMessage(chat_id, "Invalid Semester number for regular students.")
        elif student_id[1] == "2" and student_id[4] == '5':
            # Lateral entry student in batch 2021
            #if semester_no == '3':
             #   student_data = df_cse20214[df_cse20214['Student_id'] == student_id]
              #  send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            if semester_no == '4':
                student_data = df_cse20214[df_cse20214['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            elif semester_no == '5':
                student_data = df_cse20215[df_cse20215['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            elif semester_no == '6':
                student_data = df_cse20216[df_cse20216['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            else:
                bot.sendMessage(chat_id, "Invalid Semester number for lateral entry students.")
        elif student_id[1] == "2":
            # Batch 2022 regular student
            if semester_no=='3':
             student_data = df_cse20223[df_cse20223['Student_id'] == student_id]
             send_student_data(student_data, batch_no="2022", semester_no=semester_no)
            elif semester_no=='4':
                student_data = df_cse20214[df_cse20214['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            else:
                bot.sendMessage(chat_id,"Sorry Boss Check your Credentials")
        elif student_id[1] == "0":
            # Batch 2020 regular student
            if semester_no=='7':
             student_data = df_cse20207[df_cse20207['Student_id'] == student_id]
             send_student_data(student_data, batch_no="2020", semester_no=semester_no)
            elif semester_no=='8':
                student_data = df_cse20208[df_cse20208['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
        elif student_id[1]=='1' and student_id[4]=='5':
            if semester_no=='7':
                student_data = df_cse20207[df_cse20207['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            elif semester_no=='8':
                student_data = df_cse20208[df_cse20208['Student_id'] == student_id]
                send_student_data(student_data, batch_no="2021", semester_no=semester_no)
            else:
                bot.sendMessage(chat_id,"Sorry Anna Okasari Credentials Check chey")
        else:
            bot.sendMessage(chat_id, "Invalid Student ID format.")

# Initialize the Telegram bot
bot = telepot.Bot('6356204665:AAGknXTxdAwi9sbSEU9INEXzrUfgJccWSjE')
bot.deleteWebhook()

# Set up the message handler
MessageLoop(bot, handle_message).run_as_thread()

# Keep the script running
while True:
    pass
