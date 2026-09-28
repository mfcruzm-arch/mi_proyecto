from twiApliRoberto import User

print(f"{'ID':<5} | {'USUARIO':<20} | {'PASSWORD':<12} | {'BIO'}")
print("-" * 65)

for user in User.get_users():
    print(f"{user.id:<5} | {user.username:<20} | {user.password:<12} | {user.bio or ''}")
