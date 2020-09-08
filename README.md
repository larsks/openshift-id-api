## Environment variables

- `IDAPI_ADMIN_TOKEN`

  This is the password for the `admin` user.

- `IDAPI_USE_SA`

  If set, this tells `idapi` that it should authenticate using a
  `ServiceAccount`.

- `IDAPI_AUTH_DB`

  Path to authentication information. This points to a directory that
  contains one file per user, where the content of each file is the password
  for that user.

  This is meant to configured via Kubernetes secrets.

## API

### Users

- `POST /user`

  Create a new user. Payload is JSON dictionary of the form:

  ```
  {
    "user": "username",
    "full_name": "Full Name"
  }
  ```

  Returns information about the created user, or `409 CONFLICT` if the
  user already exists.


- `GET /user/<user>`

  Return information about `<user>`, or a 404 error if the user does not exist.

- `DELETE /user/<user>`

  Remove user and any associated identities.

### Projects

- `POST /project`

  Create a new project. Payload is JSON dictionary of the form:

  ```
  {
    "project": "projectname",
    "requester": "username",
    "display_name": "Display Name"
  }
  ```

  Returns information about the created project, or `409 CONFLICT` if the
  project already exists.


- `GET /project/<project>`

  Return information about `<project>`, or a 404 error if the project does not exist.

- `DELETE /project/<project>`

  Remove project.

### Roles

- `POST /project/<project>/role`

  Create a new rolebinding in `<project>`. Payload is a JSON dictionary of 
  the form:

  ```
  {
    "role": "rolename"
  }
  ```

  The `role` key may have the value `admin`, `edit`, or `view`. This will 
  create a rolebinding in `<project>` named `moc-<role>` that maps 
  associated users to the cluster role `<role>`.

- `GET /project/<project>/role/<role>`
- `DELETE /project/<project>/role/<role>`
- `POST /project/<project>/role/<role>`
- `DELETE /project/<project>/role/<role>/user/<user>`

## Examples

The following examples use the `http` command from [httpie][].

[httpie]: https://httpie.org/

### Create a new user

```
http --auth admin:secret https://idapi/user user=lars@redhat.com
```

### Create a new project

```
http --auth admin:secret https://idapi/project project=lars-example
```

### Register a user as a project admin

```
http --auth admin:secret https://idapi/project/lars-example/role/admin \
  user=lars@redhat.com
```

### Remove a project admin

```
http --auth admin:secret DELETE https://idapi/project/lars-example/role/admin/user/lars@redhat.com
```
