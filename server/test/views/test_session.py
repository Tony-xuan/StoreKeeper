from test.views import CommonSessionTest


class TestAdminCanLogin(CommonSessionTest):
    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_admin(self):
        self.assertRequest("post", "/sessions", data={"username": self._ADMIN_SET["username"],
                                                      "password": self._ADMIN_SET["password"]},
                           expected_data=self._ADMIN_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=self._ADMIN_GET)

    def test_logging_in_with_admin_with_bad_password(self):
        self.assertRequest("post", "/sessions", data={"username": self._ADMIN_SET["username"],
                                                      "password": "bad_%s" % self._ADMIN_SET["password"]},
                           expected_status_code=401)


class TestLoginWithoutActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=self._USER1_SET)
        self.assertRequestAsAdmin("post", "/users", data=self._USER2_SET)

    def test_no_sessions(self):
        self.assertRequest("get", "/sessions", expected_status_code=401)

    def test_logging_in_with_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": self._USER1_SET["username"],
                                                      "password": self._USER1_SET["password"]},
                           expected_data=self._USER1_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=self._USER1_GET)

    def test_logging_in_with_non_existed_user(self):
        self.assertRequest("post", "/sessions", data={"username": "not_exist",
                                                      "password": "orange"},
                           expected_status_code=401)

    def test_logging_in_with_existed_user_with_bad_password(self):
        self.assertRequest("post", "/sessions", data={"username": self._USER1_SET["username"],
                                                      "password": "bad_%s" % self._USER1_SET["password"]},
                           expected_status_code=401)

    def test_logging_cant_happen_without_active_session(self):
        self.assertRequest("delete", "/sessions", expected_status_code=401)


class TestLoginWithActiveSession(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=self._USER1_SET)
        self.assertRequestAsAdmin("post", "/users", data=self._USER2_SET)
        self.assertRequest("post", "/sessions", data={"username": self._USER1_SET["username"],
                                                      "password": self._USER1_SET["password"]},
                           expected_status_code=201)

    def test_re_login_with_different_user(self):
        self.assertRequest("post", "/sessions", data={"username": self._USER2_SET["username"],
                                                      "password": self._USER2_SET["password"]},
                           expected_data=self._USER2_GET,
                           expected_status_code=201)

        self.assertRequest("get", "/sessions", expected_data=self._USER2_GET)

    def test_logout(self):
        self.assertRequest("delete", "/sessions")
        self.assertRequest("get", "/sessions", expected_status_code=401)


class TestAdminRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=self._USER1_SET)

    def test_admin_can_get_list_of_users(self):
        self.assertRequestAsAdmin("get", "/users")

    def test_admin_can_get_itself(self):
        self.assertRequestAsAdmin("get", "/users/%d" % self._ADMIN_GET["id"])

    def test_admin_can_get_another_user(self):
        self.assertRequestAsAdmin("get", "/users/%d" % self._USER1_GET["id"])

    def test_admin_can_update_itself(self):
        self.assertRequestAsAdmin("put", "/users/%d" % self._ADMIN_GET["id"], data=self._ADMIN_SET)

    def test_admin_can_update_another_user(self):
        self.assertRequestAsAdmin("put", "/users/%d" % self._USER1_GET["id"], data=self._USER1_SET)

    def test_admin_can_not_delete_itself(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % self._ADMIN_GET["id"], expected_status_code=422)

    def test_admin_can_delete_another_user(self):
        self.assertRequestAsAdmin("delete", "/users/%d" % self._USER1_GET["id"])

    def test_admin_can_get_current_session(self):
        self.assertRequestAsAdmin("get", "/sessions")


class TestUserRights(CommonSessionTest):
    def setUp(self):
        super().setUp()
        self.assertRequestAsAdmin("post", "/users", data=self._USER1_SET)
        self.assertRequest("post", "/sessions", data={"username": self._USER1_SET["username"],
                                                      "password": self._USER1_SET["password"]},
                           expected_status_code=201)

    def test_user_can_not_get_list_of_users(self):
        self.assertRequest("get", "/users", expected_status_code=403)

    def test_user_can_not_add_new_user(self):
        self.assertRequest("post", "/users", data=self._USER2_SET, expected_status_code=403)

    def test_user_can_get_itself(self):
        self.assertRequest("get", "/users/%d" % self._USER1_GET["id"])

    def test_user_can_get_another_user(self):
        self.assertRequest("get", "/users/%d" % self._ADMIN_GET["id"])

    def test_user_can_update_itself(self):
        self.assertRequest("put", "/users/%d" % self._USER1_GET["id"], data=self._USER1_SET)

    def test_user_can_not_update_another_user(self):
        self.assertRequest("put", "/users/%d" % self._ADMIN_GET["id"], data=self._ADMIN_SET, expected_status_code=403)

    def test_user_can_not_delete_itself(self):
        self.assertRequest("delete", "/users/%d" % self._USER1_GET["id"], expected_status_code=403)

    def test_user_can_not_delete_another_user(self):
        self.assertRequest("delete", "/users/%d" % self._ADMIN_GET["id"], expected_status_code=403)

    def test_user_can_get_current_session(self):
        self.assertRequest("get", "/sessions")