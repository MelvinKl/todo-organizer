import logging
import sys
import uuid

import streamlit as st

from db.schema.todo_item import TodoItem
from db.schema.todo_list import TodoList
from logic.logic import Logic
from logic.priority_update_algorithms import PriorityUpdateAlgorithms

logger = logging.getLogger(__name__)
l = Logic()

selected_list = None
task_items = []


def _save_changes(key):
    priority = st.session_state[f"{key}priority"]
    description = st.session_state[f"{key}description"]
    print(priority)
    print(description)
    relevant_item = [x for x in task_items if x.id == key][0]
    relevant_item.priority = priority
    relevant_item.description = description
    l.upsert_list(selected_list, task_items)


def _delete_list_item(key):
    relevant_item = [x for x in task_items if x.id == key][0]
    l.delete_item(relevant_item)


def _finish_list_item(key):
    relevant_item = [x for x in task_items if x.id == key][0]
    l.finish_item(selected_list, relevant_item)


def _add_new_list_item(priority, title, description, priority_update_increment_weight):
    new_item = TodoItem(list_id=selected_list.id, priority=priority, title=title, description=description,
                        priority_update_increment_weight=priority_update_increment_weight)
    l.upsert_list(selected_list, task_items + [new_item])


def _add_new_list(name, max_priority, priority_update_algorithm):
    new_list = TodoList(id=str(uuid.uuid4()), name=name, priority_max=max_priority,
                        priority_update_algorithm=priority_update_algorithm.value)
    l.upsert_list(new_list, [])


with st.sidebar:
    selected_list = st.selectbox('TODO Lists', l.get_all_lists())

    with st.expander("New List", expanded=False):
        with st.form(key="new_list_form"):
            name = st.text_input(label="Name")
            max_priority = st.number_input(label="Priority", min_value=0.,
                                           max_value=sys.float_info.max,
                                           step=1., value=5.)
            priority_update_algorithm = st.selectbox("Priority update Algorithm", PriorityUpdateAlgorithms)
            submitted = st.form_submit_button("Add")
            if submitted:
                _add_new_list(name, max_priority, priority_update_algorithm)
                st.rerun()

    if selected_list:
        st.markdown("""---""")
        with st.expander("New Item", expanded=False):
            with st.form(key="new_item_form"):
                priority = st.number_input(label="Priority", min_value=0.,
                                           max_value=selected_list.priority_max,
                                           step=0.1, value=0.)
                if selected_list.priority_update_algorithm == PriorityUpdateAlgorithms.Increment.value:
                    priority_update_increment_weight = st.number_input(label="Priority increment value", min_value=0.,
                                                                       max_value=5., step=.01)
                else:
                    priority_update_increment_weight = 0
                title = st.text_input(label="Title")
                description = st.text_area(label="Description")
                submitted = st.form_submit_button("Add")
                if submitted:
                    _add_new_list_item(priority, title, description, priority_update_increment_weight)

        st.markdown("""---""")
        if st.button(key="delete_list", label="Delete list"):
            l.delete_item(selected_list)

if selected_list:
    task_items = l.get_list_items(selected_list)
    st.title(selected_list.name)

# for task in db.items:
for task in task_items:
    # print(task.id)
    st.session_state[f"{task.id}_priority"] = task.priority
    st.session_state[f"{task.id}_description"] = task.description
    with st.expander(task.title, expanded=False):
        new_priority = st.number_input(label="Priority", min_value=0.,
                                       max_value=selected_list.priority_max,
                                       step=0.1,
                                       value=st.session_state[f"{task.id}_priority"], key=f"{task.id}priority",
                                       on_change=_save_changes, args=(task.id,)
                                       )
        new_description = st.text_area(label="Description", value=st.session_state[f"{task.id}_description"],
                                       key=f"{task.id}description", on_change=_save_changes, args=(task.id,))
        col1, col2 = st.columns(2)
        with col1:
            st.button(label="Delete", key=f"{task.id}delete", on_click=_delete_list_item, args=(task.id,))
        with col2:
            st.button(label="Finish", key=f"{task.id}finish", on_click=_finish_list_item, args=(task.id,))
