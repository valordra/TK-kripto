import tkinter

from generate_prime_number import generate_prime_number
from get_primitive_root import find_primitive
from sympy.ntheory.residue_ntheory import primitive_root
from tkinter import *
from tkinter import messagebox


class GUI:
    def __init__(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.window.title("Diffie hellman Key Exchange")
        self.window.geometry("600x300")
        self.frame.pack()

        def cmd():
            self.generate()

        generate_button = Button(self.frame, text="Generate Prime", font="CourierNew 9", command=cmd)
        generate_button.grid(row=0, column=2, pady=10)

        self.window.mainloop()

    def generate(self):
        q = generate_prime_number()
        prime_label = Label(self.frame, text="q = " + str(q), font="Arial 10 bold")
        prime_label.grid(row=1, column=2)

        a = primitive_root(q)
        root_label = Label(self.frame, text="a = " + str(a), font="Arial 10 bold")
        root_label.grid(row=2, column=2, pady=(2, 5))

        alice = Label(self.frame, text="Alice", font="Arial 11 bold")
        alice.grid(row=3, column=0, sticky="W")
        alice_private_label = Label(self.frame, text="Xa", font="Arial 9")
        alice_private_label.grid(row=4, column=0, padx=(5, 1), sticky="W")
        alice_private = Entry(self.frame)
        alice_private.grid(row=4, column=1, sticky="W")

        bob = Label(self.frame, text="Bob", font="Arial 11 bold")
        bob.grid(row=3, column=3, sticky="W")
        bob_private_label = Label(self.frame, text="Xb", font="Arial 9")
        bob_private_label.grid(row=4, column=3, sticky="W")
        bob_private = Entry(self.frame)
        bob_private.grid(row=4, column=4, padx=(1, 5), sticky="W")

        def cmd():
            Xa = alice_private.get()
            Xb = bob_private.get()
            error_messages = []
            if len(Xa) <= 0 or len(Xb) <= 0:
                error_messages.append("Key can't be empty")
            if len(Xa) < 10 or len(Xb) < 10:
                error_messages.append("Key must be 10 digits or more")
            try:
                if int(Xa) >= q or int(Xb) >= q:
                    error_messages.append("Key must be less than prime")
            except ValueError:
                error_messages.append("Key must be decimal digits")
            try:
                assert (len(error_messages) == 0)
                self.simulate(q, a, int(Xa), int(Xb))
            except AssertionError:
                tkinter.messagebox.showerror('Key Error', "\n".join(error_messages))

        simulate_button = Button(self.frame, text="Simulate", font="CourierNew 8", command=cmd)
        simulate_button.grid(row=9, column=2, pady=5)

    def simulate(self, q: int, a: int, Xa: int, Xb: int):
        alice_public = create_public_key(a, Xa, q)
        bob_public = create_public_key(a, Xb, q)

        alice_public_label_formula = Label(self.frame, text="Ya", font="Arial 10")
        alice_public_label_formula.grid(row=5, column=0, padx=(5, 0), sticky="W")
        alice_public_label_formula = Label(self.frame, text="= a^Xa mod q", font="Arial 10")
        alice_public_label_formula.grid(row=5, column=1, sticky="W")
        alice_public_label = Label(self.frame, text="= " + str(alice_public), font="Arial 10")
        alice_public_label.grid(row=6, column=1, sticky="W")

        bob_public_label_formula = Label(self.frame, text="Yb", font="Arial 10")
        bob_public_label_formula.grid(row=5, column=3, sticky="W")
        bob_public_label_formula = Label(self.frame, text="= a^Xb mod q", font="Arial 10")
        bob_public_label_formula.grid(row=5, column=4, padx=(0, 5), sticky="W")
        bob_public_label = Label(self.frame, text="= " + str(bob_public), font="Arial 10")
        bob_public_label.grid(row=6, column=4, padx=(0, 5), sticky="W")

        alice_session = create_session_key(bob_public, Xa, q)
        bob_session = create_session_key(alice_public, Xb, q)

        alice_session_label_formula = Label(self.frame, text="K", font="Arial 10")
        alice_session_label_formula.grid(row=7, column=0, padx=(5, 0), sticky="W")
        alice_session_label_formula = Label(self.frame, text="= Yb^Xa mod q", font="Arial 10")
        alice_session_label_formula.grid(row=7, column=1, sticky="W")
        alice_session_label = Label(self.frame, text="= " + str(alice_session), font="Arial 10")
        alice_session_label.grid(row=8, column=1, sticky="W")

        bob_session_label_formula = Label(self.frame, text="K", font="Arial 10")
        bob_session_label_formula.grid(row=7, column=3, sticky="W")
        bob_session_label_formula = Label(self.frame, text="= Ya^Xb mod q", font="Arial 10")
        bob_session_label_formula.grid(row=7, column=4, padx=(0, 5), sticky="W")
        bob_session_label = Label(self.frame, text="= " + str(bob_session), font="Arial 10")
        bob_session_label.grid(row=8, column=4, padx=(0, 5), sticky="W")


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
