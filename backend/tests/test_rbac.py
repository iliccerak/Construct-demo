from application.auth.rbac import has_permission


def test_has_permission_allows_super_admin():
    assert has_permission("super_admin", "company.create")


def test_has_permission_blocks_worker_company_create():
    assert not has_permission("worker", "company.create")
