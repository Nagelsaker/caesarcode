from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import argparse
import os



# ===============================================================================================
#   Dataclasses 
# ===============================================================================================

@dataclass(frozen=True)
class Alphabet:
    id: str
    length: int
    data: tuple

    def __getitem__(self, index: int) -> Any:
        return self.data[index]

    def index(self, value: Any) -> int:
        return self.data.index(value)

    def __contains__(self, value: Any) -> bool:
        return value in self.data

@dataclass(frozen=True)
class Norwegian(Alphabet):
    id: str = "no"
    length: int = 29
    data: tuple[str] = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                       "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                       "u", "v", "w", "x", "y", "z", "æ", "ø", "å")

@dataclass(frozen=True)
class English(Alphabet):
    id: str = "en"
    length: int = 26
    data: tuple[str] = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                       "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                       "u", "v", "w", "x", "y", "z")


ALPHABETS = {
    "no": Norwegian(),
    "en": English(),
}


# /==============================================================================================

# ===============================================================================================
#   I/O
# ===============================================================================================

def verify_alphabet_length(a_id: str) -> None:
    alphabet = ALPHABETS.get(a_id)
    if alphabet.length != len(alphabet.data):
        print(f"{alphabet.id} alphabet length inconsitent: {alphabet.length}, {len(alphabet.data)}")
    

def load_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def save_text(filepath: str, text: str, decrypt: bool) -> None:
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    prefix = "DEC_" if decrypt else "ENC_"
    save_path = os.path.join(directory, prefix + filename)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"File saved to {save_path}\n")


# /==============================================================================================

# ===============================================================================================
#   Caesar code encryption / decryption
# ===============================================================================================


def encrypt_letter(p: str, alphabet: Alphabet, k: int) -> str:
    '''
    eₖ,ₗ(p) = (p + k) mod l
    '''
    e = alphabet[(alphabet.index(p.lower()) + k) % alphabet.length]
    e = e.upper() if p != p.lower() else e
    return e


def decrypt_letter(c: str, alphabet: Alphabet, k: int) -> str:
    '''
    dₖ,ₗ(c) = (c − k) mod l
    '''
    d = alphabet[(alphabet.index(c.lower()) - k) % alphabet.length]
    d = d.upper() if c != c.lower() else d
    return d


def encrypt(text: str, alphabet: Alphabet, k: int) -> str:
    enc_list = []
    for p in text:
        if p.lower() in alphabet:
            enc_list.append(encrypt_letter(p, alphabet, k))
        else:
            enc_list.append(p) # Appends non alphabetical letters
    encrypted = "".join(enc_list)

    return encrypted


def decrypt(text: str, alphabet: Alphabet, k: int) -> str:
    dec_list = []
    for c in text:
        if c.lower() in alphabet:
            dec_list.append(decrypt_letter(c, alphabet, k))
        else:
            dec_list.append(c) # Appends non alphabetical letters
    decrypted = "".join(dec_list)

    return decrypted


# /==============================================================================================



def main(args):
    filepath = args.filepath
    a_id = args.alphabet
    k = args.k
    should_decrypt = args.decrypt

    alphabet = ALPHABETS.get(a_id)
    if alphabet is None:
        print(f"Unknown alphabet '{a_id}, Available: {list(ALPHABETS.keys())}")
        return
    
    text = load_text(filepath)

    if should_decrypt:
        decrypted = decrypt(text, alphabet, k)
        save_text(filepath, decrypted, should_decrypt)
        print(f"{decrypted}")
    else:
        encrypted = encrypt(text, alphabet, k)
        save_text(filepath, encrypted, should_decrypt)
        print(f"{encrypted}")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Caesar cipher")
    parser.add_argument("filepath", type=str)
    parser.add_argument("alphabet", type=str, help="Alphabet id, e.g. 'no', 'en'")
    parser.add_argument("k", type=int, help="Shift value")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt instead of encrypt")
    args = parser.parse_args()
    main(args)
