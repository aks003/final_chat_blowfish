import blowfish as bf
bf.init()
data=int(input("Enter the input "))
data_encrypted = bf.encrypt(data)
print("Encrypted data is: ",data_encrypted)
print("Hex value :",hex(data_encrypted))
data_decrypted = bf.decrypt(data_encrypted)

print("Data after decryption is : ",data_decrypted) 