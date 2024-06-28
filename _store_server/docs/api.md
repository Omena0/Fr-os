
# Api documentation

## Reading

This section regards all the formating that I've used in this document.

### Data types

The types of data used in this document

    lowerCamelCase = Variable
    UPPERCASE = Static string
    <WRAPPEDSTR> = The "replace me with X"

### Variables

Variable information

    display_name     - Display name
    name - Unique identifier
    Password - MD5 hash of password
    Token    - MD5 hash we use for identification.

### Errors

Protocol responses

    INVALID         - Invalid file/app id

### Operators

Logical operators used in this document

    && - And   - Different pieces of data separated by "|"
    || - Or    - Server will respond with either of the specified responses

### Format

Request format

    # <REQUEST NAME>
      <DESCRIPTION>
      <CONVERSATION>

## Requests

### GET_APPS

Gets all apps

```
CLIENT -> GET_APPS
SERVER -> <list:apps>
```

### GET_APP

Gets information about an app

```
CLIENT -> GET_APP && <app_id>
SERVER -> <app_name> && <app_description> && <app_download_id> && <app_banner_id> && <app_icon_id>
```

### GET_FILE

Gets a file

```
CLIENT -> GET_FILE && <file_id>
SERVER -> <FILETRANSFER>
```
