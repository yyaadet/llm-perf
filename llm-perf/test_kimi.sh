#!/bin/sh

token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMTA2ODcwOSwiaWF0IjoxNzExMDY3ODA5LCJqdGkiOiJjbnVkNThlY3A3ZjRzbXRkcmQ1ZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNudGNucmN1ZHU2ZjhhYjVoYWcwIiwic3BhY2VfaWQiOiJjbnRjbnJjdWR1NmY4YWI1aGFmZyIsImFic3RyYWN0X3VzZXJfaWQiOiJjbnRjbnJjdWR1NmY4YWI1aGFmMCJ9.4vndtdnCP8bfJZdr4E7kMaGhqlKAfJjkZgp8X62Qp5b8a3Zkyh0cbF6l_v9FQaYxnT2PqqxaXy-zhzqQnOy11g'
cookie='_ga=GA1.1.677245371.1706074495; _ga_YXD8W70SZP=GS1.1.1711066837.13.1.1711066840.0.0.0; Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b=1711066838; Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b=1710554021,1710934976,1710985910,1711057747; Hm_lvt_4532beacc312859e0aa3e4a80566b706=1709544817; _ga_31QPQG2YYD=GS1.1.1706074494.1.1.1706074510.0.0.0'

python run.py kimi \
  --cookie "${cookie}" \
  --token "${token}" \
  --chat_id 'cnu2g683r073gl10nc4g'
