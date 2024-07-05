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

> **Campaign Token**: To obtain `YOUR_CAMPAIGN_TOKEN`, register on the [RecomPI panel](https://panel.recompi.com/clients/sign_in). After registration, [add a campaign](https://panel.recompi.com/campaigns/new) in the panel, and a campaign token will be generated instantly. Use this token as your API key in the code.

### Pushing User Behavior

Use the `push` method to send user interaction data to the RecomPI API. You can include tags, profiles, location, and geographical information.

```python
from recompi import RecomPI, Tag, Profile, SecureProfile, Location, Geo

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
- `profiles` (list[Profile|SecureProfile] or Profile|SecureProfile): List of `Profile` or `SecureProfile` objects or a single `Profile` or a single `SecureProfile`.
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
print(response)  # [success: true] {'click': {'18': 0.25, '19': 0.75}, 'buy': {'13': 0.89, '95': 0.11}}
```

#### Parameters

- `labels` (list[str]): List of event labels for which recommendations are requested.
- `profiles` (list[Profile|SecureProfile] or Profile|SecureProfile, optional): List of `Profile` or `SecureProfile` objects or a single `Profile` or a single `SecureProfile`.
- `geo` (Geo, optional): A `Geo` object containing geographical information.

#### Explanation of Response:
The response structure (`{'click': {'18': 0.25, '19': 0.75}, 'buy': {'13': 0.89, '95': 0.11}}`) indicates:
- For the `click` label, the user is predicted to engage more with `Tag.id = 19` (with a probability of `0.75`) compared to `Tag.id = 18` (`0.25`).
- For the `buy` label, the user is likely to make a purchase with `Tag.id = 13` (`0.89` probability) rather than `Tag.id = 95` (`0.11` probability).

These predictions are derived from the user's past interactions (`click` and `buy` events) and other factors such as their profile attributes and geographical location. The recommendation engine uses this data to suggest items or actions that are likely to be of interest to the user, helping to optimize engagement or conversions based on predictive analytics.

### Verifying API Connectivity

Use the `verify` method to check if the API key and configuration are correct.

```python
from recompi import RecomPI

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN")
response = api.verify()
print("API is well configured and connected?", response.is_success())  # [success: true]
```

### Usage with SecureProfile

You can use `SecureProfile` to ensure that sensitive information such as user IDs are hashed before being sent to the API. This adds an extra layer of security by obfuscating the actual IDs.

```python
from recompi import RecomPI, Tag, SecureProfile, Location, Geo

api = RecomPI(api_key="YOUR_CAMPAIGN_TOKEN", hash_salt="SOME_HASH_SALT")
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
    profiles=SecureProfile(name="user_id", id="123"),
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
- `profiles` (list[Profile|SecureProfile] or Profile|SecureProfile): List of `Profile` or `SecureProfile` objects or a single `Profile` or a single `SecureProfile`.
- `location` (Location, optional): A `Location` object containing IP, URL, referer, and user-agent information.
- `geo` (Geo, optional): A `Geo` object containing geographical information like country and province.

### Additional Details:

- **Initialization**: `SecureProfile` is initialized with `name` and `id`. It extends the base `Profile` to add the capability of hashing the `id`.
- **`to_json` Method**: This method converts the `SecureProfile` instance to a JSON-compatible dictionary, hashing the `id` if a `hash_salt` is provided. This is useful for securely sending profile data.
- **`recom`**: If you use `SecureProfile` in the `push` method, you must also use `SecureProfile` to retrieve data with the `recom` method. This ensures the consistency of hashed data between sending and retrieving.


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

profile = Profile(name="user_id", id="123")

print(profile.to_json())  # {'user_id': '123'}
```

#### SecureProfile

Represents a user profile with a secure ID and name.

```python
from recompi import SecureProfile

profile = SecureProfile(name="user_id", id="123")

print(profile.to_json())  # {'user_id': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
print(profile.to_json("SOME_HASH_SALT"))  # {'user_id': 'e6ee87b7300073f85bc86d817b6656d58443b23438faacc6737bde461ecf38cd'}
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