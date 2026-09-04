import uuid

import streamlit as st


SESSION_KEY = "resume_genie_session_id"


def get_session_id() -> str:
    """
    Return a persistent guest session ID.

    The session ID is stored in Streamlit session state
    and persisted in the browser using a URL query parameter.
    """

    if SESSION_KEY not in st.session_state:

        query_params = st.query_params

        existing_session_id = query_params.get(
            SESSION_KEY
        )

        if existing_session_id:

            st.session_state[SESSION_KEY] = (
                existing_session_id
            )

        else:

            new_session_id = str(
                uuid.uuid4()
            )

            st.session_state[SESSION_KEY] = (
                new_session_id
            )

            st.query_params[SESSION_KEY] = (
                new_session_id
            )

    return st.session_state[SESSION_KEY]