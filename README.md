# tradepy
## refer https://upstox.com/developer/api-documentation/

## Using the package:
### Clone the repo

### import library
from upstox import Upstox

### Replace .env file with your tokens or replace your tokens in the code
API_KEY=***
API_SECRET=***
CLIENT_ID=***

### open this url to get code, Replace with your API_KEY:
"https://api.upstox.com/v2/login/authorization/dialog?client_id=" + API_KEY + "&redirect_uri=https://www.google.com"

### The code would be in the last part of the redirected link, copy paste the code below
code = "code"

### initialise the client
upstox_client = Upstox(code)

### Get profile info
res = upstox_client.get_profile()

### Get fund balance
res = upstox_client.get_fund()

### Get day's trade
res = upstox_client.get_days_trade()

### Get ltp of an instrument
res = upstox_client.get_ltp(['NSE_EQ|INE848E01016'])

### Get intraday ohlc
res = upstox_client.get_intrday_ohlc('NSE_EQ|INE848E01016','1minute')
interval allowed = '1minute','30minute'

### Get historical data
res = upstox_client.get_historical_data('NSE_EQ|INE848E01016','1minute','2024-01-01','2023-12-31')
interval allowed = '1minute','30minute','day','day','week','month'

### get options contract
res = upstox_client.get_option_contracts('NSE_INDEX|Nifty 50','2024-07-04')





