# from datetime import date,timedelta
# from datetime import datetime

# a = '30 September'
# b = '1 October'
# c = '2 h'
# d = '40 m'
# e = '2 d'
# f = '29 April at 14:03'

# from datetime import date,timedelta
# from datetime import datetime
# current_date = date.today()
# def formate_date(posted_date):

#     if (' at' in posted_date):
#         posted_date = posted_date.split(' at')[0]

#     if (' h' in posted_date) or (' m' in posted_date):
#         return current_date

#     elif (' d' in posted_date):
#         posted_date = posted_date.split(' d')[0]
#         posted_date = current_date - timedelta(days=int(posted_date))
#         return posted_date

#     elif any(['January' in posted_date, 'February' in posted_date , 'March' in posted_date , 'April' in posted_date , \
#         'May' in posted_date ,'June' in posted_date , 'July' in posted_date , 'August'\
#         in posted_date , 'September' in posted_date , 'October' in posted_date , 'November' in posted_date , 'December' in posted_date]):
   
#         posted_day, month_name = posted_date.split()[0],posted_date.split()[1]
#         mnum = datetime.strptime(month_name, '%B').month
#         posted_date = str(date.today().year) + '-' + ( "0"+str(mnum) if mnum < 10 else str(mnum) ) +  '-' +( posted_day if int(posted_day) >= 10 else '0'+posted_day)
#         return posted_date


# print(formate_date(f))



    







    
    





