import json

import streamlit as st

from sdk import ContractWatcher, ContractWatcherException

if 'sdk' not in st.session_state:
    with st.form('login'):
        st.caption('# Login')

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        submitted = st.form_submit_button('Submit')

        if submitted:
            try:
                st.session_state.sdk = ContractWatcher(username, password)
                st.experimental_rerun()
            except ContractWatcherException as ex:
                st.warning(ex.msg)

    st.stop()

st.set_page_config(layout="wide")

sdk = st.session_state.sdk
webhook_tab, history_tab = st.tabs(['# Webhooks', '# History'])

with webhook_tab:
    c1, c2 = st.columns([2, 1])

    with c1:
        st.table(sdk.webhooks())

    with c2:
        with st.form('delete_webhook'):
            st.caption('# Delete webhook')

            wid = st.text_input("Id")

            submitted = st.form_submit_button('Submit')

            if submitted:
                try:
                    if '..' in wid:
                        w1, w2 = wid.split('..')
                        w1, w2 = int(w1), int(w2)

                        for i in range(w1, w2 + 1):
                            sdk.delete_webhook(i)
                    else:
                        wid = int(wid)
                        sdk.delete_webhook(wid)
                    st.experimental_rerun()

                except ValueError:
                    st.warning("Wid is not a range or digit")

        with st.form('create_webhook'):
            st.caption('# Create webhook')

            address = st.text_input('Address')
            event = st.text_input('Event')
            url = st.text_input('Url')
            label = st.text_input('Label')

            abi = st.text_area('Contract abi')

            submitted = st.form_submit_button('Submit')

            if submitted:
                try:
                    abi = json.loads(abi)
                    sdk.create_webhook(address, event, url, label, abi)
                    st.experimental_rerun()
                except json.JSONDecodeError:
                    st.warning('Invalid abi')


with history_tab:
    st.json(sdk.history())
