# ducky-interactions

## Get Started

1. Create a file config.json
2. Create a field "discord" like this
```json
{
  "discord": {
    "client_id": "client id goes here",
    "client_secret": "client secret goes here",
    "token": "token goes here",
    "public_key": "public key goes here"
  }
}
```
3. Install the requirements by using `pip install -U -r requirements.txt`
4. Expose the webserver to the internet. It's recommended to use a proxy like Caddy or nginx, but for local testing, something like ngrok or localhost.run can suffice.
5. Enter the full ip/address to the Interactions Endpoint field in the Discord Dev portal, followed by /interactions
6. Start the application by using the provide 
8. Done, your application should now respond to Discord slash commands