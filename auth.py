from authlib.integrations.requests_client import OAuth2Session

# Fournisseur OAuth (exemple pour GitHub)
client_id = 'votre_client_id'
client_secret = 'votre_client_secret'
authorize_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

# Création de la session OAuth2
session = OAuth2Session(client_id, client_secret, redirect_uri='http://localhost:5000/callback')

# Obtenir l'URL d'autorisation
authorization_url, state = session.create_authorization_url(authorize_url)
print("Ouvrez ce lien dans le navigateur pour autoriser l'application:", authorization_url)

# Après redirection de l'utilisateur, récupération du token d'accès
def get_token(authorization_response):
    token = session.fetch_token(token_url, authorization_response=authorization_response)
    return token
