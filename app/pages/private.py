import streamlit as st
import requests
import jwt
import urllib.parse

redirect_uri = "http://localhost:8501/private"

def is_logged_in():
    if (
        "id_token" in st.session_state
        and st.session_state.id_token is not None
    ):
        return True
    return False


if "code" in st.query_params:
    third_step_url = (
        f"{st.secrets.kc.base_int_url}"
        + f"/realms/{st.secrets.kc.realm}/protocol/openid-connect/token"
    )

    body = {
        "client_id": st.secrets.kc.client_id,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code": st.query_params["code"],
    }

    response = requests.post(third_step_url, data=body)
    json = response.json()

    if "id_token" in json:
        st.session_state.id_token = json["id_token"]
        id_token_decoded = jwt.decode(
            json["id_token"], options={"verify_signature": False}
        )

        st.session_state.id_token = json["id_token"]
        st.session_state.name = id_token_decoded["name"]


if not is_logged_in():
    redirect_uri = "http://localhost:8501/private"
    first_step_url = (
        f"{st.secrets.kc.base_ext_url}"
        + f"/realms/{st.secrets.kc.realm}/protocol/openid-connect/auth?"
        + f"client_id={st.secrets.kc.client_id}&"
        + f"redirect_uri={urllib.parse.quote(redirect_uri, safe='')}&"
        + "response_type=code&scope=openid"
    )

    st.html(
        f'<a href="{first_step_url}" target="_self">Click here to connect</a>'
    )

else:
    st.header(f"Hello, {st.session_state.name}", divider="grey")
    st.text("This page is private")
