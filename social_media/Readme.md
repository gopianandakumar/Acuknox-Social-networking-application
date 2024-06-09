{
  "info": {
    "name": "Social Networking API",
    "description": "API endpoints for the social networking application",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "User Signup",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"email\": \"user@example.com\",\n    \"password\": \"password123\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "http://localhost:8000/user/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "user"
          ]
        }
      },
      "response": []
    },
    {
      "name": "User Login",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"email\": \"user@example.com\",\n    \"password\": \"password123\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "http://localhost:8000/user/login/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "user",
            "login"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Send Friend Request",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"to_user_id\": 2\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "http://localhost:8000/friend-requests/send_request/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "friend-requests",
            "send_request"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Accept Friend Request",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/friend-requests/{friend_request_id}/accept_request/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "friend-requests",
            "{friend_request_id}",
            "accept_request"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Reject Friend Request",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/friend-requests/{friend_request_id}/reject_request/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "friend-requests",
            "{friend_request_id}",
            "reject_request"
          ]
        }
      },
      "response": []
    },
    {
      "name": "List Friends",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/friend-requests/list_friends/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "friend-requests",
            "list_friends"
          ]
        }
      },
      "response": []
    },
    {
      "name": "List Pending Friend Requests",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/friend-requests/list_pending_requests/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "friend-requests",
            "list_pending_requests"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Logout",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Token your-auth-token",
            "type": "text"
          }
        ],
        "url": {
          "raw": "http://localhost:8000/user/logout/",
          "protocol": "http",
          "host": [
            "localhost"
          ],
          "port": "8000",
          "path": [
            "user",
            "logout"
          ]
        }
      },
      "response": []
    }
  ]
}
end point s
