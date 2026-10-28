
import streamlit as st

from src.screens.home_screen import home_screen as _home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog


def _render_home_screen_ui():
    st.title('SnapClass')
    st.caption('Making Attendance faster using AI')
    st.markdown(
        """
        <div style="padding: 1rem 1.25rem; border-radius: 0.8rem; background: rgba(49,51,63,0.06); margin-bottom: 1.5rem;">
            <strong>Welcome to SnapClass</strong><br>
            Create classes, take attendance faster, and keep your students engaged with AI-powered check-ins.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('For teachers')
        st.write('Create classrooms, share join codes, and review attendance reports seamlessly.')
    with col2:
        st.subheader('For students')
        st.write('Join a class with a code and check in instantly without a slow manual process.')

    st.write('')
    teacher_col, student_col = st.columns(2)
    with teacher_col:
        if st.button('Login as Teacher', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    with student_col:
        if st.button('Login as Student', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()


def _make_home_method(method_name):
    def _method(self, *args, **kwargs):
        return _render_home_screen_ui()
    return _method


if isinstance(_home_screen, type):
    for method_name in list(getattr(_home_screen, '__abstractmethods__', set())):
        setattr(_home_screen, method_name, _make_home_method(method_name))
    home_screen = _home_screen
else:
    def home_screen():
        _render_home_screen_ui()


def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
main()