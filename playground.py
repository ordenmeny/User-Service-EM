import jwt


with open("certs/jwt-private.pem", "r", encoding="utf-8") as f:
    private_key = f.read()


with open("certs/jwt-public.pem", "r", encoding="utf-8") as f:
    public_key = f.read()


encoded_jwt = jwt.encode(
    {
        "some": "payload",
    },
    private_key,
    algorithm="RS256",
)


decoded = jwt.decode(
    encoded_jwt,
    public_key,
    algorithms=["RS256"],
)

print(decoded)