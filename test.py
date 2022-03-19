from tkinter import *
import urllib.parse
import urllib.request
import requests

'=============================FIRST WINDOW FUNCTION==============================='


def find_books_results():
    search_word = textinput1.get()
    url = ('https://www.googleapis.com/books/v1/volumes?&' + urllib.parse.urlencode({'q': search_word}) + '\
&OrderBy=relevance&maxResults=10&printType=books')
    apiresult = requests.get(url)
    parseddoc = apiresult.json()

    print(parseddoc)

    x = 1
    for thing in parseddoc['items']:
        title = thing['volumeInfo']['title']
        try:
            desc = thing['volumeInfo']['description']
        except KeyError:
            desc = "None"
        try:
            subtitle = thing['volumeInfo']['subtitle']
        except KeyError:
            subtitle = 'None'
        try:
            category = thing['volumeInfo']['categories'][0]
        except KeyError:
            category = 'None'
        try:
            authors = thing['volumeInfo']['authors'][0]
        except KeyError:
            authors = 'None'
        final_str = '%d. \nTitle:  %s \nSubtitle: %s\nCategory: %s\nAuthor: %s\n' % \
                    (x, title, subtitle, category, authors)
        label.insert(END, final_str + '\n')
        x = x + 1


'===============================FIRST WINDOW VARIABLES==============================='

window = Tk()
window.title("Bonder™️ - Find Your Book!")
window.iconbitmap(r'icon.ico')

var = StringVar()
var.set('thisisnothing')

canvas = Canvas(window, height=830, width=600)
canvas.pack()

background_image = PhotoImage(file='landscape.png')
background_label = Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

'==================================================================================='

textinput1 = StringVar()

frame = Frame(window, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.05, anchor='n')

input1 = Entry(frame, bg='white', cursor='dot', font=40, textvariable=textinput1)
input1.place(relwidth=0.65, relheight=1)

button = Button(frame, text="Press me nigga", font=40, command=find_books_results)
button.place(relx=0.7, relwidth=0.3, relheight=1)

'==================================================================================='

lower_frame = Frame(window, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.6, anchor='n')

label = Text(lower_frame, bg='white')
label.place(relwidth=1, relheight=1)

'=================================FIRST WINDOW===================================='


def create_window():

    '============================SECOND WINDOW FUNCTION============================'

    def find_prod_results():
        key = 'Yesuudei-NCTUComp-PRD-5bddb6120-7f94bd0e'

        wear = clicked.get()
        choice_prod = choice.get()
        search_word1 = textinput1.get()
        maxprice_res = maxprice.get()
        num_res = num.get()

        if wear == 'New':
            wear = 1000
            wear = str(wear)
        elif wear == 'New with Defects':
            wear = 1750
            wear = str(wear)
        elif wear == 'Manufacturer refurbished':
            wear = 2000
            wear = str(wear)
        elif wear == 'Used':
            wear = 3000
            wear = str(wear)
        elif wear == 'Very Good':
            wear = 4000
            wear = str(wear)
        elif wear == 'Good':
            wear = 5000
            wear = str(wear)
        elif wear == 'Acceptable':
            wear = 6000
            wear = str(wear)

        url = ('https://www.googleapis.com/books/v1/volumes?&' + urllib.parse.urlencode({'q': search_word1}) + '\
&OrderBy=relevance&maxResults=10&printType=books')
        apiresult = requests.get(url)
        parseddoc = apiresult.json()

        y = 0
        for thing in parseddoc['items']:
            if y == choice_prod:
                break
            try:
                full_title = thing['volumeInfo']['title'] + " " + thing['volumeInfo']['subtitle']
                if len(full_title) > 98:
                    try:
                        full_title = thing['volumeInfo']['title'] + " " + thing['volumeInfo']['authors'][0]
                    except KeyError:
                        full_title = thing['volumeInfo']['title']

            except KeyError:
                try:
                    full_title = thing['volumeInfo']['title'] + " " + thing['volumeInfo']['authors'][0]
                    y = y + 1
                except KeyError:
                    full_title = thing['volumeInfo']['title']
                    y = y + 1
                continue

            y = y + 1
            if y == choice_prod:
                break

        print(full_title)

        search_word = full_title

        url = ('http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=findItemsByKeywords\
&sortOrder=PricePlusShippingLowest\
&buyerPostalCode=92128&SERVICE-VERSION=1.13.0\
&SECURITY-APPNAME=' + key + '\
&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&CategoryName=Books\
&aspectFilter.aspectName=Books\
&itemFilter(0).name=Condition\
&itemFilter(0).value=' + wear + '\
&itemFilter(1).name=MaxPrice\
&itemFilter(1).value=' + maxprice_res + '\
&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=USD\
&keywords=' + search_word)

        apiresult = requests.get(url)
        parseddoc = apiresult.json()

        json_status = parseddoc['findItemsByKeywordsResponse'][0]['ack'][0]
        Items_found = parseddoc['findItemsByKeywordsResponse'][0]['searchResult'][0]['@count']

        divider = '============================================================================================================'
        Items_found_str = '%s Items Found!\n%s\n\n' % (Items_found, divider)

        label3.insert(END, Items_found_str )

        x = 0
        title_prev = 'thisisnothing'
        repeat = 'no'
        a = 1
        try:
            piece = parseddoc["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
            for item in piece:
                title = item["title"][0]
                bookLink = item['viewItemURL'][0]
                if repeat == 'no':
                    if title == title_prev:
                        continue

                price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']

                final_str = '%d.\n%s [%s$]\neBay Link: %s\n' % (a, title, price, bookLink)
                label3.insert(END, final_str + '\n')

                title_prev = title
                x = x + 1
                if x == num_res:
                    break
                a = a + 1
        except KeyError:
            b = 'Unfortunately, there are no books with the parameters you have specified.\n\n' \
                'Please restart your variables by pressing [Click to Proceed!] in the window: Part I\n\n' \
                'If this keeps happening please consider a different book, because the book you are looking ' \
                'for may not be available at the moment.\n\n' \
                'Press [Click to Exit!] and search for another amazing book!\n\n'
            label3.insert(END, b)

        '===============================FIRST WINDOW VARIABLES==============================='

    def close_window():
        window.destroy()
        window2.destroy()

    '==================================SECOND WINDOW===================================='

    global button3
    global background_image2
    global background_label2

    '===================================================================================='

    window2 = Toplevel()
    window2.title("Bonder™️ - Find Your Book!")
    window2.iconbitmap(r'icon.ico')

    canvas2 = Canvas(window2, height=830, width=1000)
    canvas2.pack()

    background_image2 = PhotoImage(file='landscape.png')
    background_label2 = Label(window2, image=background_image2)
    background_label2.place(relwidth=1, relheight=1)

    '===================================================================================='

    choice = IntVar()

    frame_half = Frame(window2, bg='#80c1ff', bd=5)
    frame_half.place(relx=0.27, rely=0.1, relwidth=0.43, relheight=0.05, anchor='n')

    label_half = Label(frame_half, text='Choose the Book You Like', bg='white', font='Sans 11')
    label_half.place(relwidth=0.65, relheight=1)

    input_half = Entry(frame_half, bg='white', cursor='dot', font=40, textvariable=choice)
    input_half.place(relx=0.7, relwidth=0.3, relheight=1)

    '===================================================================================='

    num = IntVar()

    frame2 = Frame(window2, bg='#80c1ff', bd=5)
    frame2.place(relx=0.73, rely=0.1, relwidth=0.43, relheight=0.05, anchor='n')

    label2a = Label(frame2, text='Enter Number of Books to be Displayed', bg='white', font='Sans 11')
    label2a.place(relwidth=0.65, relheight=1)

    input2 = Entry(frame2, bg='white', cursor='dot', font=40, textvariable=num)
    input2.place(relx=0.7, relwidth=0.3, relheight=1)

    '===================================================================================='

    maxprice = StringVar()

    frame3 = Frame(window2, bg='#80c1ff', bd=5)
    frame3.place(relx=0.27, rely=0.17, relwidth=0.43, relheight=0.05, anchor='n')

    label3 = Label(frame3, text='Enter How Much Money You Have', bg='white', font='Sans 11')
    label3.place(relwidth=0.65, relheight=1)

    input3 = Entry(frame3, bg='white', cursor='dot', font=40, textvariable=maxprice)
    input3.place(relx=0.7, relwidth=0.3, relheight=1)

    label3a = Label(input3, text='$', bg='white', font='Sans 11')
    label3a.place(relx=0.8, relwidth=0.2, relheight=1)

    '==================================================================================='

    frame4 = Frame(window2, bg='#80c1ff', bd=5)
    frame4.place(relx=0.73, rely=0.17, relwidth=0.43, relheight=0.05, anchor='n')

    button3 = Button(frame4, text="Search", font=40, command=find_prod_results)
    button3.place(relx=0.7, relwidth=0.3, relheight=1)

    options = [
        "New",
        "New with Defects",
        "Manufacturer refurbished",
        "Used",
        "Very Good",
        "Good",
        "Acceptable"
    ]

    clicked = StringVar()
    clicked.set("Choose The Wear of Your Book")

    drop = OptionMenu(frame4, clicked, *options)
    drop.place(relwidth=0.65, relheight=1)

    '==================================================================================='

    frame5 = Frame(window2, bg='#80c1ff', bd=10)
    frame5.place(relx=0.5, rely=0.24, relwidth=0.89, relheight=0.58, anchor='n')

    label3 = Text(frame5, bg='white')
    label3.place(relwidth=1, relheight=1)
    # label3.config(fg='blue')
    # Print results in here

    '==================================================================================='

    button4 = Button(window2, text="Click to Exit!", font=40, command=close_window)
    button4.place(relx=0.5, rely=0.89, relwidth=0.89, relheight=0.05, anchor='s')


'===============================END OF SECOND WINDOW=================================='

# For first window, not second!
button2 = Button(window, text="Click to Proceed!", font=40, command=create_window)
button2.place(relx=0.5, rely=0.89, relwidth=0.75, relheight=0.05, anchor='s')


mainloop()

