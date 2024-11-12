from repositories import authentication

def seed():
    authentication.batch_insert(
        [
            {
                "id": 1,
                "username": "ann.ke",
                "email": "ann.ke@gmail.com",
                "hashed_password": "$2b$12$CRwUvYvvyPz6Ef93AEY/fOR9pprgs24W2Oq762UefSMjFy2TO01CS"
            }
        ]
    )