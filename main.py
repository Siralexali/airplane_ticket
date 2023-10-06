import requests
import jdatetime
from datetime import date


def city(origin, destination):
    city = {"آبادان": "ABD", "آقاجاری": "AKW", "ابوموسی": "AEU", "اراک": "AJK", "اردبیل": "ADU", "ارومیه": "OMH",
             "اصفهان": "IFN",
             "امیدیه": "OMI", "اهواز": "AWZ", "ایران شهر": "IHR", "ایلام": "IIL", "بابلسر": "BBL", "بجنورد": "BJB",
             "بم": "BXR",
             "بندر عباس": "BND", "بندر لنگه": "BDH", "بندر ماهشهر": "MRX", "بهرگان": "IAQ", "بوشهر": "BUZ",
             "بیرجند": "XBJ",
             "بیشه کلا": "BSM", "پارس آباد": "PFQ", "تبریز": "TBZ", "تبس": "TCX", "تهران": "THR", "توحید": "TEW",
             "جزیره خارک": "KHK", "جزیره سیری": "SXI", "جزیره کیش": "KIH", "جیرفت": "JYR", "چابهار": "ZBR",
             "خانه": "KHA",
             "خرم آباد": "KHD", "خوی": "KHY", "دزفول": "DEF", "رامسر": "RZR", "رشت": "RAS", "رفسنجان": "RJN",
             "زابل": "ACZ",
             "زاهدان": "ZAH", "زنجان": "JWN", "ساری": "SRY", "سبزوار": "AFZ", "سرخس": "CKT", "سنندج": "SDG",
             "سهند": "ACP",
             "سیرجان": "SYJ", "شهر کرد": "CQD", "شیراز": "SYZ", "عسلویه": "PGU", "فاسا": "FAZ", "قزوین": "GZW",
             "قشم": "GSM",
             "گچساران": "GCH", "گورگن": "GBT", "لار": "LRR", "لامرد": "LFM", "لاوان": "LVP", "مشهد": "MHD",
             "نوژه": "NUJ",
             "نوشهر": "NSH", "هسا": "IFH", "همدان": "HDM", "هوادریا": "HDR", "کانگان": "KNR", "کرمان": "KER",
             "کرمانشاه": "KSH", "کلاله"
             : "KLM", "یاسوج": "YES", "یزد": "AZD", }
    out = [0, 0]
    out[0] = city.get(origin)
    out[1] = city.get(destination)
    return (out)


def check_age(birthday):
    birthday = str(birthday).split('-')
    today_date = str(date.today()).split('-')
    days = ((int(today_date[0]) - int(birthday[0])) * 365) + ((int(today_date[1]) - int(birthday[1])) * 30) + (
                int(today_date[2]) - int(birthday[2]))
    if days <= 365 * 2:
        return ('INF')
    elif days > 365 * 2 and days < 365 * 12:
        return ('CHD')
    elif days > 365 * 12:
        return ('ADL')


def edit_date(inp):
    inp = inp.split('-')
    return (str(jdatetime.date(day=int(inp[2]), month=int(inp[1]), year=int(inp[0])).togregorian()))


def enter_origin_and_distination():
    origin = input("please enter your origin city.\n")
    destination = input("please enter your destination city.\n")
    return [origin, destination]


def start():
    manual() if input(
        "1- the earliest ticket(buy automaticaly)\n2- buy manual ticket\nplease choose your way\n") == '2' else auto()


def enter_time():
    date_of_flight = input("please enter date.     like this ----> year-month-day\n").split('-')
    return (jdatetime.date(day=int(date_of_flight[2]), month=int(date_of_flight[1]),
                           year=int(date_of_flight[0])).togregorian())


def manual():
    org_des = enter_origin_and_distination()
    org_des = city(org_des[0],org_des[1])
    flight_time = enter_time()
    out = city(org_des[0], org_des[1])
    count_of_pass = count_of_passengers()
    data = flight_list(count_of_pass,org_des,flight_time)
    can_select = search_in_flights(data)
    if can_select != []:
        choose_flight(can_select,count_of_pass)



def auto():
    org_des = enter_origin_and_distination()

def count_of_passengers():
    return input("please enter count of passengers   like this ----> adult count-child count-infant count\n").split("-")

def flight_list(count_of_pass,org_des,calender):
    url = "https://flight.atighgasht.com/api/Flights"
    payload = {
        "AdultCount": count_of_pass[0],
        "Baggage": "true",
        "ChildCount": count_of_pass[1],
        "InfantCount": count_of_pass[2],
        "CabinClass": "All",
        "Routes": [
            {
                "OriginCode": org_des[0],
                "DestinationCode": org_des[1],
                "DepartureDate": str(calender)
            }
        ]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data

    else:
        print("Error:", response.status_code)


def search_in_flights(data):
    counter = 1
    can_select = []
    for flights in data['Flights']:
        if flights['Prices'] != []:
            print(flights['Segments'][0]['Legs'][0]['DepartureTime'][11:16] + " ---> " +
                  flights['Segments'][0]['Legs'][0][
                      'ArrivalTime'][11:16] + "  " +
                  flights['Segments'][0]['Legs'][0]['Airline']['PersianTitle'] + " -" + str(counter))
            counter += 1
            can_select.append(flights)
    return can_select

def choose_flight(can_select,count_of_pass):
    time = input("please choose a time\n")
    ProposalId = can_select[int(time) - 1]["Prices"][0]["ProposalId"]
    reserve(ProposalId,count_of_pass,can_select,time)

def reserve(ProposalId,count_of_pass,can_select,time):
    url = 'https://flight.atighgasht.com/api/Flights/Reserve'
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJidXMiOiI0ZiIsInRybiI6IjE3Iiwic3JjIjoiMiJ9.vvpr9fgASvk7B7I4KQKCz-SaCmoErab_p3csIvULG1w',
        'content-type': 'application/json-patch+json',
    }
    payload = {
        'AdultCount': count_of_pass[0],
        'ChildCount': count_of_pass[1],
        'InfantCount': count_of_pass[2],
        'CabinClass': can_select[int(time) - 1]["Prices"][0]['CabinClass'],
        'DiscountToken': '',
        'ProposalId': ProposalId,
        'Baggage': True,
    }


    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        need_bill = response.json()
        get_information(count_of_pass,need_bill)
    else:
        print("Error:", response.status_code)

def get_information(count_of_pass,need_bill):
    passengers = []
    for tmp in range(int(count_of_pass[0]) + int(count_of_pass[1]) + int(count_of_pass[2])):
        passenger = {'FirstName': input("please enter your firstname\n"),
                     'LastName': input("please enter your lasttname\n"),
                     'Male': True if input("please enter your gender(male or female)\n") == 'male' else False,
                     'NationalCode': input("please enter your nationalcode\n"),
                     'BirthDay': edit_date(input("please enter your birthday(like that : year-month-day)\n")),
                     }
        passenger.update({'PaxType': check_age(passenger['BirthDay'])})
        passengers.append(passenger)

    PhoneNumber = input("please enter your phone number  like this -----> 9171234543\n")
    PhoneNumber = '0' + PhoneNumber

    bill(passengers,PhoneNumber,need_bill)

def bill(passengers,PhoneNumber,need_bill):
    url = "https://bill.mrbilit.ir/api/Bills"
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJidXMiOiI0ZiIsInRybiI6IjE3Iiwic3JjIjoiMiJ9.vvpr9fgASvk7B7I4KQKCz-SaCmoErab_p3csIvULG1w',
        'content-type': 'application/json-patch+json',
        'x-playerid': '5de41ba3-32fc-4809-b4c1-18a95a6fb245',
    }
    payload = {
        'Person': passengers,
        'Bill': {
            'Id': need_bill['BillId'],
            'Email': '',
            'Mobile': PhoneNumber,
            'SecondaryMobile': PhoneNumber,
        },
        'ByPassPaxCountValidation': False,
        'Message': '',
    }

    response = requests.post(url, headers=headers, json=payload)
    final = response.json()
    print('https://payment.mrbilit.ir/api/billpayment/' + final[
        'BillCode'] + '?payFromCredit=false&access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJidXMiOiI0ZiIsInRybiI6IjE3Iiwic3JjIjoiMiJ9.vvpr9fgASvk7B7I4KQKCz-SaCmoErab_p3csIvULG1w')


start()






