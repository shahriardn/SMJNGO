from django.test import TestCase

services = {
        "service_title": ["کمک هزینه درمانی ", "hello","by"],
        "service_disc" :["کمک میکنیم خخخخخخ","منسشتب","منتسیتبم"]

    }
# sss= ["کمک هزینه درمانی ", "hello","by","fkjs","falksf","askf","fjasklf"]
# print(len(sss))
for p in range(len(services["service_title"])):
    print(services["service_title"][p], "...........", services["service_disc"][p])
