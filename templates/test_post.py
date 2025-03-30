import requests
#верный
job = {
    "team_leader": 1,
    "job": "1",
    "id": 1,
    "work_size": 1,
    "collaborators": "1",
    "start_date": "1",
    "end_date": "1",
    "is_finished": True,

}
print(requests.post("http://127.0.0.1:5000/api/jobs",json=job).json())
#с пустым запросом
job1 = {
    "team_leader": 1,
    "job": "1",
    "id": 1,
    "work_size": "",
    "collaborators": "1",
    "start_date": "1",
    "end_date": "1",
    "is_finished": True,

}
print(requests.post("http://127.0.0.1:5000/api/jobs",json=job1).json())
#с не всеми полями
job2 = {
    "team_leader": 1,
    "job": "1",
    "id": 1,
    "work_size": 1,
    "collaborators": "1",

}
print(requests.post("http://127.0.0.1:5000/api/jobs",json=job2).json())
#неправельный тип
job3 = {
    "team_leader": 1,
    "job": "1",
    "id": 1,
    "work_size": 1,
    "collaborators": 123,
    "start_date": "1",
    "end_date": "1",
    "is_finished": "True",

}
print(requests.post("http://127.0.0.1:5000/api/jobs",json=job3).json())