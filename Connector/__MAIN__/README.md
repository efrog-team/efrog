# Connector

## Requests

* ### POST "/users" — create a user
    * Request headers:
        * empty
    * Request body:
        * username: string
        * email: string
        * name: string
        * password: string
    * Request parameters:
        * empty
    * Response body:
        * empty


* ### POST "/token" — create an access token
    * Request headers:
        * empty
    * Request body:
        * username: string
        * password: string
    * Request parameters:
        * empty
    * Response body:
        * token: string (access token)

* ### GET "/users/me" — get an active user
    * Request headers:
        * Authroization: string (access token)
    * Request body:
        * empty
    * Request parameters:
        * empty
    * Response body:
        * username: string
        * email: string
        * name: string

* ### GET "/users/{username}" — get a user
    * Request headers:
        * empty
    * Request body:
        * empty
    * Request parameters:
        * username: string
    * Response body:
        * username: string
        * email: string
        * name: string

* ### POST "/teams" — create a team
    * Request headers:
        * Authroization: string (access token)
    * Request parameters:
        * empty
    * Request body:
        * name: string
    * Response body:
        * empty

* ### POST "/teams/{team_name}/team-members" — create a team memeber
    * Request headers:
        * Authroization: string (access token)
    * Request parameters:
        * team_name: string
    * Request body:
        * member_username: string
    * Response body:
        * empty

* ### GET "/teams/{team_name}/team-members?only_comfirmed={only_comfirmed}" — create a team memeber
    * Request headers:
        * Authroization: string (access token)
    * Request parameters:
        * team_name: string
        * only_comfirmed: boolean
    * Request body:
        * empty
    * Response body:
        * team_members: array[ {
            * username: string
            * email: string
            * name: string
            * confirmed: boolean
            } ]

* ### PUT "/teams/{team_name}/team-members/{team_member_username}/confirm" — confirm a team member
    * Request headers:
        * Authroization: string (access token)
    * Request parameters:
        * team_name: string
        * team_member_username: string
        * only_comfirmed: boolean
    * Request body:
        * empty
    * Response body:
        * empty