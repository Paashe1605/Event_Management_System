from cryptography.fernet import Fernet

# 1) Paste your key between the quotes (keep the b prefix)
KEY = b"YCS-rSEAMb9PpkGMHnzoZazFHNYfwjdWb0VR0YyaOls="

# 2) Set your encrypted file path (the .enc you downloaded)
ENC_FILE = "C:\\Users\\paara\\Downloads\\passes_export_20251128_052956.csv.enc"


# 3) Output filename for the decrypted CSV
OUT_FILE = ENC_FILE.replace(".enc", "")

def decrypt_file(key: bytes, enc_path: str, out_path: str):
  cipher = Fernet(key)
  with open(enc_path, "rb") as f:
    encrypted = f.read()
  decrypted = cipher.decrypt(encrypted)
  with open(out_path, "wb") as f:
    f.write(decrypted)
  print(f"Decrypted CSV saved to: {out_path}")

if __name__ == "__main__":
  decrypt_file(KEY, ENC_FILE, OUT_FILE)