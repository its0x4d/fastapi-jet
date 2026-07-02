from fastapi_jet.utils import name_fixer


def test_name_fixer_uses_single_pass_translation():
    assert name_fixer("a/b\\c*d") == "a_b_c_d"


def test_load_main_module_imports_project_main(tmp_path, monkeypatch):
    from fastapi_jet.project import load_main_module

    base_dir = tmp_path / "base"
    base_dir.mkdir()
    (base_dir / "main.py").write_text("INSTALLED_APPS = []\n")
    (tmp_path / "apps").mkdir()

    monkeypatch.chdir(tmp_path)
    main_module = load_main_module()
    assert hasattr(main_module, "INSTALLED_APPS")
