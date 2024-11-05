from twilio.rest import Client

account_sid = 'ACccce024270f43a7f17534c59abb6ff4c'
auth_token = 'd1ead85e75f45c2bac33f75644fa3ac6'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HX36dc82bec8137e2d7e31f358fae270a5',
  content_variables='{"1":"Name of receiver","2":"Message"}',
  to='whatsapp:+923150575122'
)

