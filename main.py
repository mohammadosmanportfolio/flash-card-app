from tkinter import *
import pandas, random, os.path, csv

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ('Arial', 40, 'italic')
WORD_FONT = ('Arial', 60, 'bold')

#when there are no more words, inform the user and shut down the app
def no_more_words():
    canvas.delete('all')
    canvas.create_image(850, 550, image=CARD_BACK, anchor='se')
    canvas.create_text(425, 150, text='No More Words', fill='black', font=TITLE_FONT)
    canvas.create_text(425, 250, text="Good Work", fill='black', font=WORD_FONT)
    window.after(5000, func=window.destroy)

#return random word tuple and its index from the list of word tuples
def get_word_and_index():
    global list_of_word_tuples
#    print(f"get word function... size of list: {len(list_of_word_tuples)}")
    if len(list_of_word_tuples) > 1:
        index = random.randint(0, len(list_of_word_tuples) - 1)
        word = list_of_word_tuples[index]
        return (word, index)
    else:
        word = list_of_word_tuples[0]
        return (word, 0)

def display_new_french_word(word):
    canvas.delete('all')
    canvas.create_image(850, 550, image=CARD_FRONT, anchor='se')
    canvas.create_text(425, 150, text='French', fill='black', font=TITLE_FONT)
    canvas.create_text(425, 250, text=f'{word}', fill='black', font=WORD_FONT)
    window.after(3000, display_english_translation)


#do everything that needs to be done after "wrong" button is pressed by user
def wrong_button_pressed():
    if len(list_of_word_tuples) <= 1:
        no_more_words()
    else:
        global current_word_tuple, current_word_index
        data = {
            'French': [current_word_tuple[0]],
            'English': [current_word_tuple[1]],
        }
        df = pandas.DataFrame(data)
        df.to_csv('data/words_to_learn.csv', mode='a', index=False, header=False)
        del list_of_word_tuples[current_word_index]
        new_word = get_word_and_index()
        current_word_tuple = new_word[0]
        current_word_index = new_word[1]
        display_new_french_word(word=current_word_tuple[0])

#do everything that needs to be done after user presses the "right" button
def right_button_pressed():
    global current_word_tuple, current_word_index
    # print(list_of_word_tuples)
    # print(f"Size of list: {len(list_of_word_tuples)}")
    # print(f"Current word info. right button function: {current_word_tuple}")
    if len(list_of_word_tuples) <= 1:
        no_more_words()
    else:
        del list_of_word_tuples[current_word_index]
        # print(f"list after deletion of item: {list_of_word_tuples}")
        new_word = get_word_and_index()
        current_word_tuple = new_word[0]
        current_word_index = new_word[1]
        display_new_french_word(word=current_word_tuple[0])

def display_english_translation():
    global canvas, current_word_tuple
    canvas.delete('all')
    canvas.create_image(850, 550, image=CARD_BACK, anchor='se')
    canvas.create_text(425, 150, text='English', fill='white', font=TITLE_FONT)
    canvas.create_text(425, 250, text=f'{current_word_tuple[1]}', fill='white', font=WORD_FONT)

#first we check if there is a "words_to_learn.csv" file. If there isn't,
#we create one. Else, if this csv file exists and it's empty, we
#create a list of word tuples using the "french_words.csv" file. If these
#two cases fail, that means the "words_to_learn.csv" file exists and
#it has words for the user, so make list of word tuples using this file
if not os.path.isfile('data/words_to_learn.csv'):
    with open('data/words_to_learn.csv', 'w') as data_csv:
        writer = csv.writer(data_csv)
        headers = ['French', 'English']
        writer.writerow(headers)
        csv_data = pandas.read_csv('data/french_words.csv')
        student_dict = csv_data.set_index('French').to_dict()['English']
        list_of_word_tuples = list(student_dict.items())
elif pandas.read_csv('data/words_to_learn.csv').empty:
    csv_data = pandas.read_csv('data/french_words.csv')
    student_dict = csv_data.set_index('French').to_dict()['English']
    list_of_word_tuples = list(student_dict.items())
else:
    csv_data = pandas.read_csv('data/words_to_learn.csv')
    student_dict = csv_data.set_index('French').to_dict()['English']
    list_of_word_tuples = list(student_dict.items())

#get the very first french word, its english translation, and its index
#in the "list_of_word_tuples" list
initial_word = get_word_and_index()
current_word_tuple = initial_word[0]
current_word_index = initial_word[1]


#======================= UI CREATION =====================================
window = Tk()
window.config(width=1000, height=1000, bg=BACKGROUND_COLOR, padx=50, pady=50)

CARD_BACK = PhotoImage(file='images/card_back.png')
CARD_FRONT = PhotoImage(file='images/card_front.png')
RIGHT_IMG = PhotoImage(file='images/right.png')
WRONG_IMG = PhotoImage(file='images/wrong.png')

canvas = Canvas(window, width=850, height=550, bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
display_new_french_word(word=current_word_tuple[0])

right_button = Button(image=RIGHT_IMG, highlightthickness=0, command=right_button_pressed)
right_button.grid(row=1, column=1)

wrong_button = Button(image=WRONG_IMG, highlightthickness=0, command=wrong_button_pressed)
wrong_button.grid(row=1, column=0)
print(len(list_of_word_tuples))

window.mainloop()