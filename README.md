# oauth2_explorator

## Demo private page

User login b.wayne / batman

## Realm export
/opt/keycloak/bin/kc.sh export --dir /tmp --users realm_file --realm gotham

## Tips

### 401 sur le userinfo

Comme le hostname est différent pour le frontchannel et le back channel les issuer dans le access token ne correspondent pas.

il faut ajouter --hostname-url=http://localhost:8080

source : https://stackoverflow.com/questions/75327787/keycloak-20-0-2-does-not-accept-backchannel-connection

L'explication ultime : https://stackoverflow.com/a/77760720

Avec mes mots si je m'adresse à keycloak en l'appelant localhost quand il va signé son token il va dire c'est moi localhost qui le signe.
Mais maintenant s'il doit vérifier que c'est bien lui qui a signé le token en se basant sur l'issuer, et qu'il n'a pas moyen de savoir qu'il sappelle localhost mais seulement de se basé sur le nom quie je lui dfonne dans mon appel donc en interne keycloak il ne pourra pas valider que c'est bien lui qu'il a délivrer le token -> 401