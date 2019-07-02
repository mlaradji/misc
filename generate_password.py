import string
import secrets

population = set().union(string.ascii_lowercase, string.ascii_uppercase, string.digits)
len_password = 20


print(f"Population size: {len(population)}. Output size: {len_password}.")
print("".join(secrets.SystemRandom().choices(tuple(population), weights=None, cum_weights=None, k=len_password)))
