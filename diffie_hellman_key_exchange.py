from generate_prime_number import generate_prime_number
from get_primitive_root import find_primitive
from tkinter import *


class GUI:
    def __init__(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.window.title("Diffie hellman Key Exchange")
        self.window.geometry("500x300")
        self.frame.pack()

        def cmd():
            self.generate()

        generate_button = Button(self.frame, text="Generate Prime", font="CourierNew 9", command=cmd)
        generate_button.grid(row=0, column=2, pady=10)
        # generate_button.place(relx=0.5, rely=0.15, anchor=CENTER)
        # generate_button.pack()

        self.window.mainloop()

    def generate(self):
        q = generate_prime_number()
        prime_label = Label(self.frame, text="q = " + str(q), font="Arial 9")
        prime_label.grid(row=1, column=2)
        # prime_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        # prime_label.pack()

        a = find_primitive(q)
        root_label = Label(self.frame, text="a = " + str(a), font="Arial 9")
        root_label.grid(row=2, column=2)
        # root_label.place(relx=0.5, rely=0.30, anchor=CENTER)
        # root_label.pack()

        alice_private = Entry(self.frame)
        alice_private.grid(row=3, column=0)

        bob_private = Entry(self.frame)
        alice_private.grid(row=3, column=4)



def input_secret_key(name: str, q: int):
    secret_key = input(f"Input {name}'s secret key (10 digits minimum): ")
    assert (len(secret_key) >= 10 and secret_key.isnumeric() and int(secret_key) < q)
    return int(secret_key)


def create_public_key(a, secret_key, q):
    return pow(a, secret_key, q)


def create_session_key(public_key, secret_key, q):
    return pow(public_key, secret_key, q)


def main():
    # setup prime (q)
    q = generate_prime_number()
    print(f"Prime is: {q}")

    # setup primitive root (a)
    a = find_primitive(q)
    print(f"Primitive root is: {a}")

    # private key min 10 digit more than q-1
    # alice
    #   choose secret key (Xa)
    alice_secret_key = input_secret_key("Alice", q)
    print(f"Alice's secret key is: {alice_secret_key}")

    # compute public key (alice)
    alice_public_key = create_public_key(a, alice_secret_key, q)
    print(f"Alice's public key is: {alice_public_key}")

    # bob
    #   choose secret key (Xb)
    bob_secret_key = input_secret_key("Bob", q)
    print(f"Bob's secret key is: {bob_secret_key}")

    # compute public key (bob)
    bob_public_key = create_public_key(a, bob_secret_key, q)
    print(f"Bob's public key is: {bob_public_key}")

    # compute shared session key (alice & bob)
    session_key_from_alice_secret = create_session_key(bob_public_key, alice_secret_key, q)
    session_key_from_bob_secret = create_session_key(alice_public_key, bob_secret_key, q)
    assert (session_key_from_bob_secret == session_key_from_alice_secret)
    print(f"Shared session key is {session_key_from_alice_secret}")


if __name__ == '__main__':
    GUI()
