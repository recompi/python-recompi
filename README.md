# RecomPI API

A Python wrapper for the RecomPI API, providing methods to interact with the service for tracking user behavior and obtaining recommendations.

## Installation

Install the RecomPI library using pip:

```bash
pip install recompi
```

## Usage

### Initialization

Create an instance of the `RecomPI` class using your campaign's API key.

```python
from recompi import RecomPI

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN")
```

### Pushing User Behavior

Use the `push` method to send user interaction data to the RecomPI API. You can include tags, profiles, location, and geographical information.

```python
from recompi import RecomPI, Tag, Profile, Location, Geo

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN")
response = api.push(
    label="click",
    tags=[
        Tag(id="1", name="Technology", desc="Technology News"),
        Tag(
            id="2",
            name="Online Marketing Tools",
            desc="Latest news on online marketing tools",
        ),
    ],
    profiles=Profile("user_id", "123"),
    location=Location(
        ip="1.1.1.1",  # Optional
        url="https://www.example.com/some/path?param1=1&param2=2",
        referer="REFERER_URL",  # Optional
        useragent="USERAGENT",  # Optional
    ),
    geo=Geo(
        country="Iran",  # Optional: 'IR' or the unique country ID
        province="Tehran",  # Optional: Any unique string
    ),  # Optional
)
print(response)  # [success: true]
```

#### Parameters

- `label` (str): A label for the event, e.g., "click".
- `tags` (list[Tag]): List of `Tag` objects representing metadata.
- `profiles` (list[Profile] or Profile): List of `Profile` objects or a single `Profile`.
- `location` (Location, optional): A `Location` object containing IP, URL, referer, and user-agent information.
- `geo` (Geo, optional): A `Geo` object containing geographical information like country and province.

### Getting Recommendations

Use the `recom` method to get recommendations based on user interactions, profiles, and geographical information.

```python
from recompi import RecomPI, Profile, Geo

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN")
response = api.recom(
    labels=["click", "buy"],
    profiles=Profile("user_id", "123"),
    geo=Geo(
        country="Iran",  # Optional: 'IR' or unique country ID
        province="Tehran",  # Optional: Any unique string
    ),
)
print(response)  # [success: true] {'مشاهده پست\u200c': {'18': 0.25, '19': 0.75}}
```

#### Parameters

- `labels` (list[str]): List of event labels for which recommendations are requested.
- `profiles` (list[Profile] or Profile, optional): List of `Profile` objects or a single `Profile`.
- `geo` (Geo, optional): A `Geo` object containing geographical information.

### Verifying API Connectivity

Use the `verify` method to check if the API key and configuration are correct.

```python
from recompi import RecomPI

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN")
response = api.verify()
print("API is well configured and connected?", response.is_success())  # [success: true]
```

### Data Structures

#### Tag

Represents a tag with an ID, name, and description.

```python
from recompi import Tag

tag = Tag(id="1", name="Technology", desc="Technology News")
```

#### Profile

Represents a user profile with an ID and name.

```python
from recompi import Profile

profile = Profile(id="user_id", name="123")
```

#### Location

Represents a location with IP, URL, referer, and user-agent information.

```python
from recompi import Location

location = Location(ip="1.1.1.1", url="https://www.example.com", referer="REFERER_URL", useragent="USERAGENT")
```

#### Geo

Represents geographical information with country and province.

```python
from recompi import Geo

geo = Geo(country="Iran", province="Tehran")
```

### Error Handling

#### RecomPIFieldTypeError

Raised when an input field does not match the expected type.

```python
from recompi import RecomPIFieldTypeError

try:
    # Some operation that might raise an error
    pass
except RecomPIFieldTypeError as e:
    print(e)
```

#### RecomPIException

General exception class for other RecomPI errors.

```python
from recompi import RecomPIException

try:
    # Some operation that might raise an error
    pass
except RecomPIException as e:
    print(e)
```

### Contributing

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

### License

This project is licensed under the MIT License.