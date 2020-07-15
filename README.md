## Boilerplate starter for building Dashboards in Plotly DASH
To acccess the URL's the parameters used here are as follows:
 - 'public_key': This parameters should contian a token as an input, generated via Fernet class from the Cryptography package.
 - 'user_id' (Optional): This parameter if to provide arguments as a data filteration paramter based on the user. 

To generate your own key pairs, use the following steps in and independent python script or a jupyter notebook.
```
pip install cryptography
```
```
private_key = Fernet.generate_key()
print(private_key)
```
Replace this printed private key in common/constants.py
```
f = Fernet(private_key)
public_key = f.encrypt(b"my deep dark secret")
print(public_key)
```
Use this public_key token in the URL parameter to access the pages of application. For example:
```
http://127.0.0.1:8005/dashboard?public_key=gAAAAABfDrRYWAmeUesF96nqTAww7TSK0sNp7WoYmYgGxp_O5XGDPPpVbE66bTYjrQrnC8ysYrLY2WmAEbpJhqg3Ntfc5igalUGwv2S1tDgZWl1BfFlyYS0=
```
OR
```
http://127.0.0.1:8005/dashboard?public_key=gAAAAABfDrRYWAmeUesF96nqTAww7TSK0sNp7WoYmYgGxp_O5XGDPPpVbE66bTYjrQrnC8ysYrLY2WmAEbpJhqg3Ntfc5igalUGwv2S1tDgZWl1BfFlyYS0=&user_id=3
```