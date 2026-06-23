# caesarcode

A simple Caesar cipher CLI for encrypting and decrypting text files.

Usage

python caesar.py <filepath> <alphabet id> <k> [-d]


Arguments

- filepath — Path to the input text file
- alphabet — Alphabet id: en (English) or no (Norwegian)
- k — Shift value (integer)
- -d — Optional flag, decrypt instead of encrypt

Examples

Encrypt:
python caesar.py textfiles/no_plain_text_01.txt no 3

Output: textfiles/ENC_no_plain_text_01.txt

Decrypt:
python caesar.py textfiles/ENC_no_plain_text_01.txt no 3 -d

Output: textfiles/DEC_ENC_no_plain_text_01.txt

Supported Alphabets

- en — English (26 letters)
- no — Norwegian (29 letters: æ, ø, å included)

Non-alphabetic characters (spaces, punctuation, numbers) are preserved unchanged.
