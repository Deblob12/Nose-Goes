# Nose-Goes — A Serverless SlackBot for Indecisive Moments
*Nose-Goes* provides an easy-to-use slash command based application that can generate POI recommendations based on individual preferences and provide travel time/directions to any location the user is interested in.


## Usage:
### Address Formatting:
All addresses should follow GoogleMaps address convention. The more fields you fill out, the less likely Nose-Goes will have issues finding your deisred Point of Interest

**Template:**
`ST_NUM, ST_NAME, NEIGHBH, CITY, STATE, ZIP, COUNTY, COUNTY_FIPS`

**Example:**
`125 Powell St, 	Union Square, San Francisco, CA, 94108, San Francisco, 06075`

### Commands:
#### Find Travel Time:
`/travel-time address1; address2`

**Example:**

![/travel-time Example](https://github.com/Deblob12/Nose-Goes/blob/master/usage/screenshots/travel-time.png "Travel-Time")

#### Get Directions (and time):
`/directions address1; address2`

**Example:**

![/directions Example](https://github.com/Deblob12/Nose-Goes/blob/master/usage/screenshots/directions.png "Directions")

#### Save Address as Nickname:
`/save nickname; address`

**Example:**

![/save Example](https://github.com/Deblob12/Nose-Goes/blob/master/usage/screenshots/save.png "Save")

## Architecture:

![Architecture](https://github.com/Deblob12/Nose-Goes/blob/master/usage/architecture/architecture.png "Architecture")
