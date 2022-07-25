'''
This file includes functions for displaying text and prompting the user for answers.
'''

'''
This comment holds brainstorming thoughts about how we might want to build a better command line UI

Do you want to download updated stock data? Yes/No

Download Fresh Data 
    Enter Ticker symbol?
    User will enter the company Ticker Symbol
    
Use Existing Data
    Get list of Tickers we want to display
    Which ticker do you want to use? (Select from the list)

Loading data as per the selected ticker

What is your investment risk tolerance?
    Low 
    Moderate 
    High

#We have no idea about how much risk each of thses strategies carry

What type of Algorithm Strategies you want to trade?
'''

from _config import *
import questionary as qt

def welcome_message():

    print()
    print('Welcome to Algo Strategy Tester')
    print()
    print("This application will let you run a pre-defined algorithmic trading strategy on stock data you select. Results are displayed in an interactive graph that you man inspect. Enjoy!")
    print()

    return None

def prompt_multiple_choice(question_text, question_options):
    '''This function wraps the Questionary .select() function used to prompt the user for an answer.
    '''

    result = qt.select(
        question_text,
        choices = question_options
    ).ask()
    print()

    return result

def prompt_single_choice(question_text):

    result = qt.confirm(question_text).ask()
    print()

    return result