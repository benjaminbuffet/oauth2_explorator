FROM quay.io/keycloak/keycloak:24.0

ENV KEYCLOAK_ADMIN=admin 
ENV KEYCLOAK_ADMIN_PASSWORD=admin 

COPY ./gotham-realm.json /opt/keycloak/data/import/

CMD [ "start-dev", "--import-realm", "--hostname-url=http://localhost:8080" ]