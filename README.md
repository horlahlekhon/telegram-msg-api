# Deepview telegram

#### To Run

we would need at least three variables to run this minimal client
* Telegram Api id
* Telegram Api hash
* Telegram username 
* Telegram phone number

to get the hash and id the user will have to be registered , each api id and api hash is 
unique to a telegram account.
to obtain the two register here  [Telegram api registeration](https://my.telegram.org/auth?to=apps)



##### clone the repo
    ```bash
        git clone https://gitlab.com/deep-view-demz/deepview-telegram.git
    ```
##### Install
Assuming there is Make, virtual env, python  > 3.6 and pip installed.
```bash
    cd deepview-telegram
    make install
```

#### run the development server

```bash
    make run
```

The development server will be started and you can call the endpoints.

### Note:
> when calling the endpoint for the first time , we would have to initiate a session,
> The endpoint `/data/get-data` should be called first and data of the user should be passed in a 
> json body like :
```json
{
	"api_hash" : "YOUR API HASH",
	"api_id": "YOUR API ID",
	"phone": "INTERNATIONAL FORMATTED PHONE NUMBER"
}
```
> then the endpoint `/telegram/sign-in` should be called with a `GET` request without a  body
> Please dont include a body. this will make the server to send a verification code to the user and after that
> `/telegram/sign-in` should be called again the second time now with a `POST` request and a body should be included that includes the code sent on the sms, like below:

 ```json
        {
            "code" : "44203"
        }
```

> this will sign the user in and create a session locally, and the user can be logged in without any login until the session expires.

##### TODO
