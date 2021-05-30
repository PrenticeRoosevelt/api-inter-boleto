from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC86486cd9b506f811f621170355816d4e"
# Your Auth Token from twilio.com/console
auth_token  = "9402db635be98e78904bd0d5aaa25bc6"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+15558675309", 
    from_="+15017250604",
    body="Hello from Python!")

print(message.sid)