import streamlit as st
import requests
import json
import urllib.parse
import jwt

tab1, tab2 = st.tabs(["auth", "well-known"])

with tab1:
    st.header("Configuration", divider="grey")
    st.json(json.dumps(dict(st.secrets.kc)))

    st.header("Step 1", divider="grey")
    first_step_url = (
        f"{st.secrets.kc.base_ext_url}"
        + f"/realms/{st.secrets.kc.realm}/protocol/openid-connect/auth?"
        + f"client_id={st.secrets.kc.client_id}&"
        + f"redirect_uri={urllib.parse.quote(st.secrets.kc.redirect_uri, safe='')}&"
        + "response_type=code&scope=openid"
    )
    st.text(first_step_url.replace("&", "&\n").replace("?", "?\n"))
    st.html(
        f'<a href="{first_step_url}" target="_self">Click here to connect</a>'
    )

    if "step" in st.query_params and st.query_params["step"] == "redirect":

        st.header("Step 2", divider="grey")

        st.write(st.query_params)

        st.header("Step 3", divider="grey")

        third_step_url = (
            f"{st.secrets.kc.base_int_url}"
            + f"/realms/{st.secrets.kc.realm}/protocol/openid-connect/token"
        )

        body = {
            "client_id": st.secrets.kc.client_id,
            "redirect_uri": st.secrets.kc.redirect_uri,
            "grant_type": "authorization_code",
            "code": st.query_params["code"],
        }
        st.subheader("Post request")
        st.write(third_step_url)
        st.write(body)

        st.subheader("Response")
        response = requests.post(third_step_url, data=body)
        json = response.json()
        st.write(json)
        access_token = None
        if "access_token" in json:
            access_token = json["access_token"]
            st.subheader("access_token")
            st.write(
                jwt.decode(access_token, options={"verify_signature": False})
            )

        if "id_token" in json:
            st.subheader("id_token")
            st.write(
                jwt.decode(
                    json["id_token"], options={"verify_signature": False}
                )
            )

        if access_token is not None:
            st.header("Step 4", divider="grey")
            header = {
                "Authorization": f"Bearer {access_token}",
            }
            userinfo_url = (
                f"{st.secrets.kc.base_url}"
                + f"/realms/{st.secrets.kc.realm}"
                + "/protocol/openid-connect/userinfo?"
            )
            userinfo_response = requests.get(
                userinfo_url,
                headers=header,
            )
            st.write(userinfo_response.status_code)
            st.write(userinfo_response.json())


with tab2:
    well_know_url = (
        f"{st.secrets.kc.base_int_url}"
        + f"/realms/{st.secrets.kc.realm}/"
        + ".well-known/openid-configuration"
    )
    response = requests.get(well_know_url)
    st.write(well_know_url)
    st.divider()
    st.write(response.json())
